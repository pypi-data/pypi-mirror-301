import { createJSONEditor } from "https://cdn.jsdelivr.net/npm/vanilla-jsoneditor@1/standalone.js";

(function init_app(global) {
  mermaid.initialize({ startOnLoad: false, useMaxWidth: true });

  Handlebars.registerHelper("json", function (context) {
    return JSON.stringify(context);
  });

  Handlebars.registerHelper("ifEquals", function (arg1, arg2, options) {
    return arg1 == arg2 ? options.fn(this) : options.inverse(this);
  });

  Handlebars.registerHelper("defaultIfEmpty", function (a, b) {
    return a ? a : b;
  });

  var panZoom = null;
  var componentSvgNodes = {};

  function drawDiagram() {
    mermaid.run({
      querySelector: "#mermaid",
      postRenderCallback: () => {
        const svgElement = document.querySelector("#mermaid>svg");
        svgElement.style.maxWidth = "";

        // Collect SVG elements which represent component nodes on the diagram
        svgElement.querySelectorAll(".component").forEach((svgElement) => {
          var [, componentId] = /flowchart-(.*)-\d+/g.exec(svgElement.id);
          componentSvgNodes[componentId] = {
            svgElement,
            labelContainer: svgElement.querySelector(".label-container"),
          };
        });

        initSvgPanZoom();
      },
    });
  }

  function changeComponentColor(componentId, color) {
    const { labelContainer } = componentSvgNodes[componentId];
    labelContainer.style.fill = color;
  }

  function initSvgPanZoom() {
    panZoom = svgPanZoom(document.querySelector("#mermaid > svg"), {
      viewportSelector: ".svg-pan-zoom_viewport",
      panEnabled: true,
      controlIconsEnabled: true,
      zoomEnabled: true,
      dblClickZoomEnabled: false, // prefer mouseWheel
      mouseWheelZoomEnabled: true,
      preventMouseEventsDefault: true,
      zoomScaleSensitivity: 0.2,
      minZoom: 0.1,
      maxZoom: 10,
      fit: true,
      contain: false,
      center: true,
    });

    panZoom.resize();
    panZoom.fit();
  }

  function resizePanZoom() {
    if (panZoom) {
      panZoom.resize();
    }
  }

  function initJsonEditor(editorSourceElement, editorTargetElement) {
    const editorSource = document.querySelector(editorSourceElement);
    const editorTarget = document.querySelector(editorTargetElement);

    return createJSONEditor({
      target: editorTarget,
      props: {
        content: {
          text: editorSource.value,
        },
        onChange: (updatedContent, _previousContent, { contentErrors }) => {
          if (!contentErrors) {
            editorSource.value = updatedContent.text;
          }
        },
        mode: "text",
        mainMenuBar: false,
        statusBar: false,
      },
    });
  }

  const pipelineInputsEditor = initJsonEditor(
    "#pipeline-inputs",
    "#pipeline-inputs-editor"
  );

  const pipelineMetadataEditor = initJsonEditor(
    "#pipeline-metadata",
    "#pipeline-metadata-editor"
  );

  function validatePipelineInputs(element) {
    const contentErrors = pipelineInputsEditor.validate();
    if (contentErrors) {
      element.setCustomValidity("invalid");
    } else {
      element.setCustomValidity("");
    }
    return true;
  }

  function validatePipelineMetadata(element) {
    const contentErrors = pipelineMetadataEditor.validate();
    if (contentErrors) {
      element.setCustomValidity("invalid");
    } else {
      element.setCustomValidity("");
    }
    return true;
  }

  var mainPanelElement = document.getElementById("main-split-panel");
  var innerPanelElement = document.getElementById("inner-split-panel");

  mainPanelElement.addEventListener("sl-reposition", resizePanZoom);
  innerPanelElement.addEventListener("sl-reposition", resizePanZoom);
  addEventListener("resize", resizePanZoom);

  document.addEventListener("DOMContentLoaded", () => {
    var mainPanelElement = document.getElementById("main-split-panel");
    var innerPanelElement = document.getElementById("inner-split-panel");

    mainPanelElement.addEventListener("sl-reposition", resizePanZoom);
    innerPanelElement.addEventListener("sl-reposition", resizePanZoom);
    addEventListener("resize", resizePanZoom);
  });

  global.pipeline_watch = {
    drawDiagram,
    changeComponentColor,
    pipelineInputsEditor,
    pipelineMetadataEditor,
    validatePipelineInputs,
    validatePipelineMetadata,
  };
})(window);
