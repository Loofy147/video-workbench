/* Local-only campaign brief/storyboard workflow. User input is inserted with textContent, never HTML. */
(() => {
  "use strict";

  const DEFAULT_SCENES = [
    { title: "Start with the business outcome", body: "Define the audience, problem, and objective before choosing the format.", duration_seconds: 3, background: "#101b2d" },
    { title: "Make the offering clear", body: "Brief, storyboard, draft video, and source-aware review in one workflow.", duration_seconds: 3, background: "#18394b" },
    { title: "Review before publication", body: "Verify claims, media rights, brand use, and approval before release.", duration_seconds: 3, background: "#26364b" }
  ];
  const form = document.querySelector("#campaign-form");
  const sceneList = document.querySelector("#scene-list");
  const projectList = document.querySelector("#project-list");
  const message = document.querySelector("#app-message");
  const saveButton = document.querySelector("#save-project");
  const renderButton = document.querySelector("#render-project");
  const artifactsPanel = document.querySelector("#artifacts-panel");
  const videoContainer = document.querySelector("#video-container");
  const renderReport = document.querySelector("#render-report");
  let selectedProjectId = null;
  let selectedProject = null;
  let busy = false;

  function showMessage(text, kind = "info") {
    message.textContent = text;
    message.dataset.kind = kind;
    message.hidden = !text;
  }

  async function api(path, options = {}) {
    const response = await fetch(path, {
      cache: "no-store",
      ...options,
      headers: { ...(options.body ? { "Content-Type": "application/json" } : {}), ...(options.headers || {}) }
    });
    const contentType = response.headers.get("content-type") || "";
    const payload = contentType.includes("application/json") ? await response.json() : null;
    if (!response.ok) throw new Error(payload?.error || `Request failed (${response.status}).`);
    return payload;
  }

  function setBusy(value) {
    busy = value;
    saveButton.disabled = value;
    renderButton.disabled = value || !selectedProjectId;
    document.querySelector("#new-project").disabled = value;
    document.querySelector("#refresh-projects").disabled = value;
    document.querySelector("#add-scene").disabled = value || sceneList.children.length >= 8;
    for (const control of form.querySelectorAll("input, textarea, button")) control.disabled = value;
    saveButton.disabled = value;
    renderButton.disabled = value || !selectedProjectId;
  }

  function makeField(labelText, control, options = {}) {
    const wrapper = document.createElement("div");
    const label = document.createElement("label");
    label.textContent = labelText;
    label.htmlFor = control.id;
    wrapper.append(label, control);
    if (options.hint) {
      const hint = document.createElement("p");
      hint.className = "muted small";
      hint.textContent = options.hint;
      wrapper.append(hint);
    }
    return wrapper;
  }

  function addScene(scene = {}, index = sceneList.children.length) {
    if (sceneList.children.length >= 8) return;
    const card = document.createElement("section");
    card.className = "scene-card";
    const header = document.createElement("div");
    header.className = "scene-card-header";
    const title = document.createElement("h3");
    title.textContent = `Scene ${index + 1}`;
    const remove = document.createElement("button");
    remove.type = "button";
    remove.className = "remove-scene";
    remove.textContent = "Remove";
    remove.setAttribute("aria-label", `Remove scene ${index + 1}`);
    remove.addEventListener("click", () => {
      card.remove();
      renumberScenes();
    });
    header.append(title, remove);

    const grid = document.createElement("div");
    grid.className = "scene-grid";
    const sceneTitle = document.createElement("input");
    sceneTitle.type = "text";
    sceneTitle.maxLength = 180;
    sceneTitle.required = true;
    sceneTitle.id = `scene-title-${crypto.randomUUID()}`;
    sceneTitle.value = scene.title || "";
    const duration = document.createElement("input");
    duration.type = "number";
    duration.min = "1";
    duration.max = "20";
    duration.step = "1";
    duration.required = true;
    duration.id = `scene-duration-${crypto.randomUUID()}`;
    duration.value = String(scene.duration_seconds ?? 3);
    const color = document.createElement("input");
    color.type = "color";
    color.id = `scene-color-${crypto.randomUUID()}`;
    color.value = /^#[0-9a-f]{6}$/i.test(scene.background || "") ? scene.background : "#101b2d";
    grid.append(
      makeField("Scene title", sceneTitle),
      makeField("Duration (seconds)", duration),
      makeField("Background", color)
    );
    const body = document.createElement("textarea");
    body.rows = 2;
    body.maxLength = 900;
    body.id = `scene-body-${crypto.randomUUID()}`;
    body.value = scene.body || "";
    const bodyField = makeField("On-screen supporting copy", body);
    card.append(header, grid, bodyField);
    sceneList.append(card);
    renumberScenes();
    document.querySelector("#add-scene").disabled = sceneList.children.length >= 8 || busy;
  }

  function renumberScenes() {
    Array.from(sceneList.children).forEach((card, index) => {
      const number = index + 1;
      card.querySelector("h3").textContent = `Scene ${number}`;
      card.querySelector(".remove-scene").setAttribute("aria-label", `Remove scene ${number}`);
      card.querySelector(".remove-scene").disabled = sceneList.children.length === 1 || busy;
    });
    document.querySelector("#add-scene").disabled = sceneList.children.length >= 8 || busy;
  }

  function collectPlan() {
    const data = new FormData(form);
    const scenes = Array.from(sceneList.children).map(card => ({
      title: card.querySelector('input[type="text"]').value.trim(),
      duration_seconds: Number(card.querySelector('input[type="number"]').value),
      background: card.querySelector('input[type="color"]').value,
      body: card.querySelector("textarea").value.trim()
    }));
    return {
      project_title: String(data.get("project_title") || "").trim(),
      offering: String(data.get("offering") || "").trim(),
      audience: String(data.get("audience") || "").trim(),
      objective: String(data.get("objective") || "").trim(),
      differentiators: String(data.get("differentiators") || "").trim(),
      call_to_action: String(data.get("call_to_action") || "").trim(),
      scenes
    };
  }

  function fillPlan(plan) {
    form.elements.project_title.value = plan.project_title || "";
    form.elements.offering.value = plan.offering || "";
    form.elements.audience.value = plan.audience || "";
    form.elements.objective.value = plan.objective || "";
    form.elements.differentiators.value = plan.differentiators || "";
    form.elements.call_to_action.value = plan.call_to_action || "";
    sceneList.replaceChildren();
    (plan.scenes && plan.scenes.length ? plan.scenes : DEFAULT_SCENES).forEach((scene, index) => addScene(scene, index));
  }

  function setProject(data) {
    selectedProjectId = data.project.id;
    selectedProject = data.project;
    fillPlan(data.plan);
    document.querySelector("#editor-heading").textContent = data.project.title;
    document.querySelector("#version-label").textContent = `Version ${data.project.version}`;
    saveButton.textContent = "Save as new version";
    renderButton.disabled = busy;
    renderButton.textContent = data.project.state === "rendering" ? "Rendering…" : "Render watermarked draft";
    artifactsPanel.hidden = false;
    document.querySelector("#brief-link").href = `/api/projects/${selectedProjectId}/files/brief`;
    document.querySelector("#campaign-link").href = `/api/projects/${selectedProjectId}/files/campaign`;
    const render = data.project.render;
    videoContainer.hidden = !render;
    renderReport.hidden = !render;
    document.querySelector("#provenance-link").hidden = !render;
    if (render) {
      const videoUrl = `/api/projects/${selectedProjectId}/files/video`;
      document.querySelector("#rendered-video").src = videoUrl;
      document.querySelector("#video-link").href = videoUrl;
      document.querySelector("#provenance-link").href = `/api/projects/${selectedProjectId}/files/provenance`;
      document.querySelector("#render-status-tag").textContent = render.release_gate?.status === "passed" ? "Release gate passed" : "Review required";
      document.querySelector("#render-details").textContent = JSON.stringify(render, null, 2);
    } else {
      document.querySelector("#render-status-tag").textContent = data.project.state === "render_failed" ? "Render failed" : "Draft saved";
      if (data.project.render_error) showMessage(data.project.render_error, "error");
    }
    refreshProjects().catch(() => {});
  }

  function resetProject() {
    selectedProjectId = null;
    selectedProject = null;
    form.reset();
    fillPlan({ scenes: DEFAULT_SCENES });
    document.querySelector("#editor-heading").textContent = "New campaign";
    document.querySelector("#version-label").textContent = "Unsaved";
    saveButton.textContent = "Create project";
    renderButton.disabled = true;
    renderButton.textContent = "Render watermarked draft";
    artifactsPanel.hidden = true;
    videoContainer.hidden = true;
    renderReport.hidden = true;
    showMessage("Start with the offering, audience, and objective. Save a project before rendering.");
  }

  async function refreshProjects() {
    const data = await api("/api/projects");
    projectList.replaceChildren();
    if (!data.projects.length) {
      const empty = document.createElement("p");
      empty.className = "muted small";
      empty.textContent = "No saved projects yet.";
      projectList.append(empty);
      return;
    }
    for (const project of data.projects) {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "project-item";
      button.setAttribute("aria-current", project.id === selectedProjectId ? "true" : "false");
      const title = document.createElement("strong");
      title.textContent = project.title;
      const updated = document.createElement("span");
      updated.textContent = `v${project.version} · ${new Date(project.updated_at).toLocaleString()}`;
      const state = document.createElement("span");
      state.className = "project-state";
      state.textContent = String(project.state || "draft").replaceAll("_", " ");
      button.append(title, updated, state);
      button.addEventListener("click", () => openProject(project.id));
      projectList.append(button);
    }
  }

  async function openProject(id) {
    if (busy) return;
    setBusy(true);
    showMessage("Opening saved project…");
    try {
      const data = await api(`/api/projects/${id}`);
      setProject(data);
      showMessage(`Opened “${data.project.title}” version ${data.project.version}.`, "success");
    } catch (error) {
      showMessage(error.message, "error");
    } finally {
      setBusy(false);
      renumberScenes();
    }
  }

  form.addEventListener("submit", async event => {
    event.preventDefault();
    if (busy || !form.reportValidity()) return;
    const plan = collectPlan();
    setBusy(true);
    showMessage(selectedProjectId ? "Saving a new project version…" : "Creating project and campaign artifacts…");
    try {
      const path = selectedProjectId ? `/api/projects/${selectedProjectId}` : "/api/projects";
      const data = await api(path, { method: selectedProjectId ? "PUT" : "POST", body: JSON.stringify(plan) });
      setProject(data);
      showMessage(`Saved version ${data.project.version}. Brief and campaign manifest are ready.`, "success");
    } catch (error) {
      showMessage(error.message, "error");
    } finally {
      setBusy(false);
      renumberScenes();
    }
  });

  renderButton.addEventListener("click", async () => {
    if (!selectedProjectId || busy) return;
    setBusy(true);
    renderButton.textContent = "Rendering…";
    showMessage("Rendering a watermarked draft locally. FFmpeg and FFprobe are validating the MP4; keep this page open.");
    try {
      const data = await api(`/api/projects/${selectedProjectId}/render`, { method: "POST", body: "{}" });
      setProject({ project: data.project, plan: collectPlan() });
      showMessage("The draft MP4 passed technical validation. The release gate remains separate and may still be blocked.", "success");
    } catch (error) {
      showMessage(error.message, "error");
      if (selectedProjectId) {
        try { setProject(await api(`/api/projects/${selectedProjectId}`)); } catch (_) { /* Keep the render error visible. */ }
      }
    } finally {
      setBusy(false);
      renderButton.textContent = "Render watermarked draft";
      renumberScenes();
    }
  });

  document.querySelector("#new-project").addEventListener("click", resetProject);
  document.querySelector("#refresh-projects").addEventListener("click", () => refreshProjects().catch(error => showMessage(error.message, "error")));
  document.querySelector("#add-scene").addEventListener("click", () => {
    if (sceneList.children.length < 8 && !busy) addScene({ title: "", body: "", duration_seconds: 3, background: "#101b2d" });
  });

  resetProject();
  refreshProjects().catch(error => showMessage(error.message, "error"));
})();
