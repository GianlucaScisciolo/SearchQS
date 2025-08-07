function displayUndisplayPassword(passwordId, buttonId) {
    const passwordField = document.getElementById(passwordId);
    const displayPasswordButton = document.getElementById(buttonId);
    if (passwordField.type === "password") {
        passwordField.type = "text";
        displayPasswordButton.innerHTML = '<i class="fa fa-eye-slash fa-2x" aria-hidden="true"></i>';
    } else {
        passwordField.type = "password";
        displayPasswordButton.innerHTML = '<i class="fa fa-eye fa-2x" aria-hidden="true"></i>';
    }
}

function enableDisableElements(arrayId) {
    arrayId.forEach(function(idElement) {
        var element = document.getElementById(idElement);
        element.disabled = !element.disabled;
    })
}

function enableDisableReadonlyElements(arrayId) {
    arrayId.forEach(function(idElement) {
        var element = document.getElementById(idElement);
        if (element.hasAttribute('readonly')) {
            element.removeAttribute('readonly');
        } else {
            element.setAttribute('readonly', true);
        }
    })
}

module.exports = { displayUndisplayPassword, enableDisableElements };

function readMoreReadLessText(index) {
    var moreText = document.getElementById("more-" + index);
    var btnText = document.getElementById("text-" + index);
    var btnIcon = document.getElementById("icon-" + index);
    var lingua = document.querySelector("#input-lingua").value;

    if (moreText.style.display === "none") {
        moreText.style.display = "inline";
        btnText.innerHTML = lingua === "italiano" ? "Nascondi codice file" : "Hide code file";
        btnIcon.classList.remove("fa-arrow-left");
        btnIcon.classList.add("fa-minus");
    } else {
        moreText.style.display = "none";
        btnText.innerHTML = lingua === "italiano" ? "Mostra codice file" : "Show code file";
        btnIcon.classList.remove("fa-minus");
        btnIcon.classList.add("fa-arrow-left");
    }
}

function showCode(index) {
  const lingua = document.getElementById('lingua').value;
  const divShowButtons = document.getElementById('div-show-buttons-'+index);
  const divCode = document.getElementById('div-code-'+index);
  const divResultStaticAnalysis = document.getElementById('div-result-static-analysis-'+index);
  const divResultsDynamicAnalysis = document.getElementById('div-results-dynamic-analysis-'+index);
  const divHideButtons = document.getElementById('div-hide-buttons-'+index);
  const showStaticAnalysisText = lingua === 'inglese' ? 'Show static analysis results' : 'Mostra risultati analisi statica';
  const showDynamicAnalysisText = lingua === 'inglese' ? "Show dynamic analysis results" : "Mostra risultati analisi dinamica";
  const hideCodeText = lingua === 'inglese' ? "Hide code file" : "Nascondi codice file";
  

  divShowButtons.innerHTML = `
    <div class="col-sm text-right" id="div-show-static-analysis-button-${index}">
      <button onclick="showStaticAnalysis('${index}')" class="custom-button" id="btn-${index}">
        <i class="fa fa-plus fa-2x" id="icon-${index}" aria-hidden="true"></i>
        <div class="icon-label" id="text-${index}">
          ${showStaticAnalysisText}
        </div>
      </button>
    </div>
    <div class="col-sm text-left" id="div-show-dynamic-analysis-button-${index}">
      <button onclick="showDynamicAnalysis('${index}')" class="custom-button" id="btn-${index}">
        <i class="fa fa-plus fa-2x" id="icon-${index}" aria-hidden="true"></i>
        <div class="icon-label" id="text-${index}">
          ${showDynamicAnalysisText}
        </div>
      </button>
    </div>
  `;

  divCode.style.display = "inline";
  divResultStaticAnalysis.style.display = "none";
  divResultsDynamicAnalysis.style.display = "none";

  divHideButtons.innerHTML = `
    <div class="col-sm text-center" id="div-hide-code-button-${index}">
      <button onclick="hideText('${index}')" class="custom-button" id="btn-${index}">
        <i class="fa fa-minus fa-2x" id="icon-${index}" aria-hidden="true"></i>
        <div class="icon-label" id="text-${index}">
          ${hideCodeText}
        </div>
      </button>
    </div>
  `;
}

function showStaticAnalysis(index) {
  const divShowButtons = document.getElementById('div-show-buttons-'+index);
  const divCode = document.getElementById('div-code-'+index);
  const divResultStaticAnalysis = document.getElementById('div-result-static-analysis-'+index);
  const divResultsDynamicAnalysis = document.getElementById('div-results-dynamic-analysis-'+index);
  const divHideButtons = document.getElementById('div-hide-buttons-'+index);
  const lingua = document.getElementById('lingua').value;
  const showCodeText = lingua === 'inglese' ? 'Show code file' : 'Mostra codice file';
  const showDynamicAnalysisText = lingua === 'inglese' ? "Show dynamic analysis results" : "Mostra risultati analisi dinamica";
  const hideStaticAnalysisText = lingua === 'inglese' ? "Hide static analysis results" : "Nascondi risultati analisi statica";
  const resultStaticAnalysis = document.getElementById("result-static-analysis-"+index).value;
  
  divShowButtons.innerHTML = `
    <div class="col-sm text-right" id="div-show-code-button-${index}">
      <button onclick="showCode('${index}')" class="custom-button" id="btn-${index}">
        <i class="fa fa-plus fa-2x" id="icon-${index}" aria-hidden="true"></i>
        <div class="icon-label" id="text-${index}">
          ${showCodeText}
        </div>
      </button>
    </div>
    <div class="col-sm text-left" id="div-show-dynamic-analysis-button-${index}">
      <button onclick="showDynamicAnalysis('${index}')" class="custom-button" id="btn-${index}">
        <i class="fa fa-plus fa-2x" id="icon-${index}" aria-hidden="true"></i>
        <div class="icon-label" id="text-${index}">
          ${showDynamicAnalysisText}
        </div>
      </button>
    </div>
  `;

  divCode.style.display = "none";
  divResultStaticAnalysis.style.display = "inline";
  divResultsDynamicAnalysis.style.display = "none";

  divHideButtons.innerHTML = `
    <div class="col-sm text-center" id="div-hide-static-analysis-button-${index}">
      <button onclick="hideText('${index}')" class="custom-button" id="btn-${index}">
        <i class="fa fa-minus fa-2x" id="icon-${index}" aria-hidden="true"></i>
        <div class="icon-label" id="text-${index}">
          ${hideStaticAnalysisText}
        </div>
      </button>
    </div>
  `;
}

function showDynamicAnalysis(index) {
  const divShowButtons = document.getElementById('div-show-buttons-'+index);
  const divCode = document.getElementById('div-code-'+index);
  const divResultStaticAnalysis = document.getElementById('div-result-static-analysis-'+index);
  const divResultsDynamicAnalysis = document.getElementById('div-results-dynamic-analysis-'+index);
  const divHideButtons = document.getElementById('div-hide-buttons-'+index);
  const lingua = document.getElementById('lingua').value;
  const showCodeText = lingua === 'inglese' ? 'Show code file' : 'Mostra codice file';
  const showStaticAnalysisText = lingua === 'inglese' ? 'Show static analysis results' : 'Mostra risultato analisi statica';
  const hideDynamicAnalysisText = lingua === 'inglese' ? "Hide dynamic analysis results" : "Nascondi risultati analisi dinamica";
  const resultsDynamicAnalysis = document.getElementById("results-dynamic-analysis-"+index).value;

  divShowButtons.innerHTML = `
    <div class="col-sm text-right" id="div-show-code-button-${index}">
      <button onclick="showCode('${index}')" class="custom-button" id="btn-${index}">
        <i class="fa fa-plus fa-2x" id="icon-${index}" aria-hidden="true"></i>
        <div class="icon-label" id="text-${index}">
          ${showCodeText}
        </div>
      </button>
    </div>
    <div class="col-sm text-left" id="div-show-static-analysis-button-${index}">
      <button onclick="showStaticAnalysis('${index}')" class="custom-button" id="btn-${index}">
        <i class="fa fa-plus fa-2x" id="icon-${index}" aria-hidden="true"></i>
        <div class="icon-label" id="text-${index}">
          ${showStaticAnalysisText}
        </div>
      </button>
    </div>
  `;

  let resultsDAHtml = '';
  for (const rda of resultsDynamicAnalysis) {
    resultsDAHtml += `<strong>${(lingua === 'inglese' ? "Quantum circuit number" : "Circuito quantistico numero") + rda.number_q_circuit}</strong>`;
  }

  divCode.style.display = "none";
  divResultStaticAnalysis.style.display = "none";
  divResultsDynamicAnalysis.style.display = "inline";

  divHideButtons.innerHTML = `
    <div class="col-sm text-center" id="div-hide-dynamic-analysis-button-${index}">
      <button onclick="hideText('${index}')" class="custom-button" id="btn-${index}">
        <i class="fa fa-minus fa-2x" id="icon-${index}" aria-hidden="true"></i>
        <div class="icon-label" id="text-${index}">
          ${hideDynamicAnalysisText}
        </div>
      </button>
    </div>
  `;
}

function hideText(index) {
  const divShowButtons = document.getElementById('div-show-buttons-'+index);
  const divCode = document.getElementById('div-code-'+index);
  const divResultStaticAnalysis = document.getElementById('div-result-static-analysis-'+index);
  const divResultsDynamicAnalysis = document.getElementById('div-results-dynamic-analysis-'+index);
  const divHideButtons = document.getElementById('div-hide-buttons-'+index);
  const lingua = document.getElementById('lingua').value;
  const showCodeText = lingua === 'inglese' ? 'Show code file' : 'Mostra codice file';
  const showStaticAnalysisText = lingua === 'inglese' ? 'Show static analysis results' : 'Mostra risultato analisi statica';
  const showDynamicAnalysisText = lingua === 'inglese' ? "Show dynamic analysis results" : "Mostra risultati analisi dinamica";

  divShowButtons.innerHTML = `
    <div class="col-sm text-right" id="div-show-code-button-${index}">
      <button onclick="showCode('${index}')" class="custom-button" id="btn-${index}">
        <i class="fa fa-plus fa-2x" id="icon-${index}" aria-hidden="true"></i>
        <div class="icon-label" id="text-${index}">
          ${showCodeText}
        </div>
      </button>
    </div>
    <div class="col-sm text-center" id="div-show-static-analysis-button-${index}">
      <button onclick="showStaticAnalysis('${index}')" class="custom-button" id="btn-${index}">
        <i class="fa fa-plus fa-2x" id="icon-${index}" aria-hidden="true"></i>
        <div class="icon-label" id="text-${index}">
          ${showStaticAnalysisText}
        </div>
      </button>
    </div>
    <div class="col-sm text-left" id="div-show-dynamic-analysis-button-${index}">
      <button onclick="showDynamicAnalysis('${index}')" class="custom-button" id="btn-${index}">
        <i class="fa fa-plus fa-2x" id="icon-${index}" aria-hidden="true"></i>
        <div class="icon-label" id="text-${index}">
          ${showDynamicAnalysisText}
        </div>
      </button>
    </div>
  `;

  divCode.style.display = "none";
  divResultStaticAnalysis.style.display = "none";
  divResultsDynamicAnalysis.style.display = "none";

  divHideButtons.innerHTML = `
  `;
}








