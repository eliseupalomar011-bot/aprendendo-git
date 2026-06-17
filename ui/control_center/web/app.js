const API = "http://localhost:8765";
const TOKEN = "TRINITY_SYSTEM_UI";

async function apiFetch(path, body = null) {
  const options = {
    method: body ? "POST" : "GET",
    headers: {
      "Content-Type": "application/json",
      "X-Trinity-Token": TOKEN
    }
  };

  if (body) options.body = JSON.stringify(body);
  return fetch(API + path, options);
}

async function loadProfile() {
  const res = await apiFetch("/power");
  const data = await res.json();
  updateProfileUI(data.profile);
}

async function setProfile(profile) {
  await apiFetch("/power", { profile });
  updateProfileUI(profile);
}

function updateProfileUI(profile) {
  document.getElementById("current").innerText =
    profile.charAt(0).toUpperCase() + profile.slice(1);
}

async function loadBrightness() {
  const res = await apiFetch("/brightness");
  const data = await res.json();
  document.getElementById("brightness").value = data.value;
}

async function setBrightness(value) {
  await apiFetch("/brightness", { value });
}

async function loadVolume() {
  const res = await apiFetch("/volume");
  const data = await res.json();
  document.getElementById("volume").value = data.value;
}

async function setVolume(value) {
  await apiFetch("/volume", { value });
}

async function toggleMute() {
  const res = await apiFetch("/mute", {});
  const data = await res.json();
  document.getElementById("volume").value = data.volume;
}

async function setAudioProfile(profile) {
  await apiFetch("/audio/profile", { profile });
  loadVolume();
}

window.onload = () => {
  loadProfile();
  loadBrightness();
  loadVolume();
};
