(function () {
  "use strict";

  const widget = document.querySelector("[data-emergency-chat-widget]");
  if (!widget) return;

  const role = widget.dataset.chatRole;
  const endpoint = widget.dataset.chatUrl;
  const websocketEndpoint = widget.dataset.chatWsUrl;
  const panel = widget.querySelector("[data-chat-panel]");
  const invite = widget.querySelector("[data-chat-invite]");
  const launcher = widget.querySelector("[data-chat-launcher]");
  const closeButton = widget.querySelector("[data-chat-close]");
  const acceptForm = widget.querySelector("[data-chat-accept-form]");
  const chatForm = widget.querySelector("[data-chat-form]");
  const bodyInput = widget.querySelector("[data-chat-body]");
  const messages = widget.querySelector("[data-chat-messages]");
  const status = widget.querySelector("[data-chat-status]");
  const unread = widget.querySelector("[data-chat-unread]");
  const recordButton = widget.querySelector("[data-chat-record]");
  const callButton = widget.querySelector("[data-chat-call]");
  const callControls = widget.querySelector("[data-call-controls]");
  const callConnection = widget.querySelector("[data-call-connection]");
  const callNote = widget.querySelector("[data-call-note]");
  const callEnd = widget.querySelector("[data-call-end]");
  const callHold = widget.querySelector("[data-call-hold]");
  const callMute = widget.querySelector("[data-call-mute]");
  const callSpeaker = widget.querySelector("[data-call-speaker]");
  const callTimer = widget.querySelector("[data-call-timer]");
  const channelButtons = widget.querySelectorAll("[data-chat-channel]");
  const fullscreen = widget.dataset.chatFullscreen === "true";
  let pollTimer;
  let presenceTimer;
  let reconnectTimer;
  let socket;
  let mediaRecorder;
  let recordingStartedAt;
  let isOpen = role === "public" || fullscreen;
  let localMuted = false;
  let speakerEnabled = false;
  let activeCall;
  let callTimerInterval;
  if (fullscreen && panel) panel.hidden = false;

  function csrfToken() {
    const input = widget.querySelector("input[name=csrfmiddlewaretoken]");
    return input ? input.value : "";
  }

  function setPanel(open) {
    isOpen = open;
    if (panel) panel.hidden = !open;
    if (launcher) launcher.setAttribute("aria-expanded", String(open));
  }

  function showStatus(message) {
    if (status) status.textContent = message;
  }

  function updateCallTimer() {
    if (!callTimer || !activeCall || activeCall.status !== "accepted" || !activeCall.started_at) {
      if (callTimer) callTimer.textContent = "00:00";
      return;
    }
    const elapsed = Math.max(0, Math.floor((Date.now() - Date.parse(activeCall.started_at)) / 1000));
    const hours = Math.floor(elapsed / 3600);
    const minutes = Math.floor((elapsed % 3600) / 60);
    const seconds = elapsed % 60;
    callTimer.textContent = (hours ? String(hours).padStart(2, "0") + ":" : "") + String(minutes).padStart(2, "0") + ":" + String(seconds).padStart(2, "0");
  }

  function renderMessages(items) {
    if (!messages) return;
    messages.replaceChildren();
    if (!items.length) {
      const empty = document.createElement("p");
      empty.className = "emergency-chat-empty";
      empty.textContent = "No messages yet. The response team will join shortly.";
      messages.appendChild(empty);
      return;
    }
    items.forEach(function (item) {
      const message = document.createElement("article");
      message.className = "emergency-chat-message" + (item.mine ? " mine" : "");

      const meta = document.createElement("small");
      meta.textContent = item.sender + " · " + item.created_at;
      message.appendChild(meta);

      if (item.body) {
        const text = document.createElement("p");
        text.textContent = item.body;
        message.appendChild(text);
      }
      if (item.audio_url) {
        const audio = document.createElement("audio");
        audio.controls = true;
        audio.preload = "metadata";
        audio.src = item.audio_url;
        message.appendChild(audio);
      }
      messages.appendChild(message);
    });
    messages.scrollTop = messages.scrollHeight;
  }

  function renderCalls(calls) {
    activeCall = calls.find(function (call) {
      return ["requested", "accepted"].includes(call.status);
    });
    const incomingCall = calls.find(function (call) {
      return call.status === "requested" && !call.mine;
    });

    if (callButton) {
      callButton.disabled = Boolean(activeCall);
      const callLabel = callButton.querySelector("small");
      const callText = activeCall
        ? (activeCall.mine ? "Voice call requested" : "Voice call active")
        : "Request voice call";
      if (callLabel) callLabel.textContent = callText;
      else callButton.textContent = callText;
    }

    if (callControls) {
      const connected = activeCall && activeCall.status === "accepted";
      callControls.hidden = !connected;
      if (connected) {
        localMuted = activeCall.mine ? activeCall.caller_muted : activeCall.recipient_muted;
        if (callConnection) callConnection.textContent = activeCall.on_hold ? "Call on hold" : "Voice call connected";
        if (callNote) {
          const remoteMuted = activeCall.mine ? activeCall.recipient_muted : activeCall.caller_muted;
          callNote.textContent = activeCall.on_hold
            ? "Both sides are on hold. Resume when ready."
            : (remoteMuted ? "The other participant is muted." : "Your secure call is active.");
        }
        if (callHold) callHold.classList.toggle("active", activeCall.on_hold);
        if (callMute) {
          callMute.classList.toggle("active", localMuted);
          callMute.querySelector("small").textContent = localMuted ? "Unmute" : "Mute";
        }
        if (callSpeaker) {
          callSpeaker.classList.toggle("active", speakerEnabled);
          callSpeaker.querySelector("small").textContent = speakerEnabled ? "Speaker on" : "Speaker";
        }
      }
    }
    updateCallTimer();

    const oldResponse = widget.querySelector("[data-call-response]");
    if (oldResponse) oldResponse.remove();
    if (!incomingCall) return;

    const response = document.createElement("div");
    response.className = "emergency-call-incoming";
    const icon = document.createElement("span");
    icon.className = "emergency-call-incoming-icon";
    icon.textContent = "☎";
    response.appendChild(icon);
    const copy = document.createElement("div");
    copy.className = "emergency-call-incoming-copy";
    const title = document.createElement("strong");
    title.textContent = "Incoming voice call";
    const detail = document.createElement("small");
    detail.textContent = role === "admin" ? "The request sender wants to speak with you." : "The response team wants to speak with you.";
    copy.appendChild(title);
    copy.appendChild(detail);
    response.appendChild(copy);
    const responseActions = document.createElement("div");
    responseActions.className = "emergency-call-incoming-actions";
    [
      ["accepted", "Accept"],
      ["declined", "Decline"],
    ].forEach(function (choice) {
      const button = document.createElement("button");
      button.type = "button";
      button.className = choice[0] === "accepted" ? "call-answer-button" : "call-decline-button";
      button.setAttribute("aria-label", choice[1] + " voice call");
      button.textContent = choice[1];
      button.addEventListener("click", function () {
        sendAction("call_response", {
          call_id: incomingCall.id,
          status: choice[0],
        });
      });
      responseActions.appendChild(button);
    });
    response.appendChild(responseActions);
    response.dataset.callResponse = "true";
    const actions = widget.querySelector(".emergency-chat-actions");
    if (actions) actions.after(response);
  }

  function applyState(data) {
    if (data.accepted && invite) invite.hidden = true;
    if (data.accepted && role === "public") setPanel(true);
    if (!data.accepted) {
      showStatus(role === "admin" ? "Waiting for the sender to accept chat." : "Accept the invitation to start chatting.");
      return;
    }
    showStatus("Messages are retained for 48 hours after this request.");
    renderMessages(data.messages || []);
    renderCalls(data.calls || []);
    if (unread) {
      unread.textContent = data.unread || "0";
      unread.hidden = !data.unread;
    }
  }

  async function refresh(markRead) {
    try {
      const refreshUrl = new URL(endpoint, window.location.origin);
      if (markRead) refreshUrl.searchParams.set("open", "1");
      const response = await fetch(refreshUrl.toString(), {
        credentials: "same-origin",
        headers: { Accept: "application/json" },
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || "Chat is unavailable.");
      applyState(data);
    } catch (error) {
      showStatus(error.message);
    }
  }

  function websocketUrl() {
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    return protocol + "//" + window.location.host + websocketEndpoint;
  }

  function connectWebSocket() {
    if (!websocketEndpoint || !window.WebSocket || (socket && socket.readyState === WebSocket.OPEN)) return;
    socket = new WebSocket(websocketUrl());
    socket.addEventListener("open", function () {
      socket.send(JSON.stringify({action: "sync"}));
      refresh(isOpen);
      showStatus("Live secure channel connected.");
    });
    socket.addEventListener("message", function (event) {
      const data = JSON.parse(event.data);
      if (data.type === "chat.state") applyState(data.state);
      if (data.type === "chat.refresh") refresh(isOpen);
      if (data.type === "chat.error") showStatus(data.error);
    });
    socket.addEventListener("close", function (event) {
      socket = null;
      if ([4001, 4403, 4404, 4409].includes(event.code)) {
        showStatus("The secure chat session is no longer available.");
        return;
      }
      window.clearTimeout(reconnectTimer);
      reconnectTimer = window.setTimeout(connectWebSocket, 3000);
    });
  }

  async function sendAction(action, values, file) {
    const payload = Object.assign({}, values || {});
    if (action === "message" && !payload.idempotency_key) {
      payload.idempotency_key = window.crypto && window.crypto.randomUUID
        ? window.crypto.randomUUID()
        : String(Date.now()) + "-" + Math.random().toString(16).slice(2);
    }
    const formData = new FormData();
    formData.append("csrfmiddlewaretoken", csrfToken());
    formData.append("action", action);
    Object.entries(payload).forEach(function (entry) {
      formData.append(entry[0], entry[1]);
    });
    if (file) formData.append("audio", file, "emergency-note.webm");
    try {
      const response = await fetch(endpoint, {
        method: "POST",
        body: formData,
        credentials: "same-origin",
        headers: { Accept: "application/json" },
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || "The chat action could not be completed.");
      applyState(data);
    } catch (error) {
      showStatus(error.message);
    }
  }

  async function startRecording() {
    if (mediaRecorder) {
      mediaRecorder.stop();
      return;
    }
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      showStatus("Audio recording is not supported on this device.");
      return;
    }
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const chunks = [];
      mediaRecorder = new MediaRecorder(stream);
      recordingStartedAt = Date.now();
      const recordLabel = recordButton.querySelector("small");
      if (recordLabel) recordLabel.textContent = "Stop recording";
      else recordButton.textContent = "Stop recording";
      showStatus("Recording audio note…");
      mediaRecorder.addEventListener("dataavailable", function (event) {
        if (event.data.size) chunks.push(event.data);
      });
      mediaRecorder.addEventListener("stop", function () {
        stream.getTracks().forEach(function (track) { track.stop(); });
        const duration = Math.max(1, Math.round((Date.now() - recordingStartedAt) / 1000));
        const audio = new Blob(chunks, { type: mediaRecorder.mimeType || "audio/webm" });
        mediaRecorder = null;
        const finishedLabel = recordButton.querySelector("small");
        if (finishedLabel) finishedLabel.textContent = "Audio note";
        else recordButton.textContent = "Record audio";
        sendAction("message", { audio_duration: duration }, audio);
      });
      mediaRecorder.start();
    } catch (error) {
      showStatus("Microphone access was not granted.");
    }
  }

  if (launcher) launcher.addEventListener("click", function () { setPanel(!isOpen); refresh(true); });
  if (closeButton) closeButton.addEventListener("click", function () { setPanel(false); });
  if (acceptForm) acceptForm.addEventListener("submit", function (event) {
    event.preventDefault();
    sendAction("accept");
  });
  if (chatForm) chatForm.addEventListener("submit", function (event) {
    event.preventDefault();
    const body = bodyInput.value.trim();
    if (!body) return;
    bodyInput.value = "";
    sendAction("message", { body: body });
  });
  channelButtons.forEach(function (button) {
    button.addEventListener("click", function () {
      const channel = button.dataset.chatChannel;
      channelButtons.forEach(function (item) { item.classList.toggle("active", item === button); });
      if (channel === "text" && bodyInput) bodyInput.focus();
      if (channel === "audio") startRecording();
      if (channel === "call") sendAction("call");
    });
  });
  if (callEnd) callEnd.addEventListener("click", function () {
    if (activeCall) sendAction("call_response", { call_id: activeCall.id, status: "ended" });
  });
  if (callHold) callHold.addEventListener("click", function () {
    if (activeCall) sendAction("call_control", { call_id: activeCall.id, control: activeCall.on_hold ? "resume" : "hold" });
  });
  if (callMute) callMute.addEventListener("click", function () {
    if (!activeCall) return;
    localMuted = !localMuted;
    sendAction("call_control", { call_id: activeCall.id, control: localMuted ? "mute" : "unmute" });
  });
  if (callSpeaker) callSpeaker.addEventListener("click", function () {
    speakerEnabled = !speakerEnabled;
    callSpeaker.classList.toggle("active", speakerEnabled);
    callSpeaker.querySelector("small").textContent = speakerEnabled ? "Speaker on" : "Speaker";
    showStatus(speakerEnabled ? "Speaker mode enabled for this device." : "Speaker mode disabled.");
  });

  refresh(role === "public");
  connectWebSocket();
  pollTimer = window.setInterval(function () {
    if (!socket || socket.readyState !== WebSocket.OPEN) refresh(isOpen);
  }, 5000);
  presenceTimer = window.setInterval(function () {
    if (socket && socket.readyState === WebSocket.OPEN) socket.send(JSON.stringify({action: "presence"}));
  }, 60000);
  callTimerInterval = window.setInterval(updateCallTimer, 1000);
  window.addEventListener("beforeunload", function () {
    window.clearInterval(pollTimer);
    window.clearInterval(presenceTimer);
    window.clearTimeout(reconnectTimer);
    window.clearInterval(callTimerInterval);
    if (socket) socket.close();
  });
})();
