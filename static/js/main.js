/* Meaning Search Lab - frontend JS (jQuery, per HW10 spec) */

$(function () {
  // ---------- Quiz: option selection ----------
  let $selected = null;

  $('.msl-option').on('click', function () {
    $('.msl-option').removeClass('selected');
    $(this).addClass('selected');
    $selected = $(this);
    $('#msl-submit').prop('disabled', false);
  });

  // ---------- Quiz: submit answer ----------
  $('#msl-submit').on('click', function () {
    if (!$selected) return;

    const qNum  = parseInt($('#msl-question').data('q-num'), 10);
    const choice = $selected.data('option-id');

    $.ajax({
      url: '/api/quiz/answer',
      method: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({ q_num: qNum, choice: choice })
    }).done(function (resp) {
      renderFeedback(resp);
    }).fail(function () {
      alert('Could not submit answer. Please refresh the page.');
    });
  });

  // ---------- Render feedback inline ----------
  function renderFeedback(resp) {
    const fb = resp.feedback;
    const $main = $('.msl-main');

    $('body').removeClass('quiz-mode');
    $('body').addClass(resp.correct ? 'feedback-correct' : 'feedback-incorrect');

    const bannerHTML = resp.correct
      ? `<div class="msl-feedback-banner ok">&#10003; Correct!</div>`
      : `<div class="msl-feedback-banner bad">&times; Not quite \u2014 let's review</div>`;

    let bodyHTML = '';
    if (resp.correct) {
      bodyHTML += `<div class="msl-feedback-card">
                     <h3 class="ok">${escapeHtml(fb.title)}</h3>`;
      if (fb.why_correct && fb.why_correct.length) {
        bodyHTML += '<h5>Why this answer:</h5><ul>';
        fb.why_correct.forEach(function (line) {
          bodyHTML += `<li>${escapeHtml(line)}</li>`;
        });
        bodyHTML += '</ul>';
      }
      if (fb.why_others && fb.why_others.length) {
        bodyHTML += '<h5>Why not the others:</h5><ul>';
        fb.why_others.forEach(function (line) {
          bodyHTML += `<li>${escapeHtml(line)}</li>`;
        });
        bodyHTML += '</ul>';
      }
      bodyHTML += '</div>';
    } else {
      bodyHTML += `<div class="msl-feedback-card">
                     <h3 class="bad">${escapeHtml(fb.title)}</h3>`;
      if (fb.review) {
        fb.review.forEach(function (item) {
          bodyHTML += `<h5>${escapeHtml(item.heading)}</h5>
                       <p>${escapeHtml(item.body)}</p>`;
        });
      }
      if (fb.summary) {
        bodyHTML += `<p><strong>${escapeHtml(fb.summary)}</strong></p>`;
      }
      bodyHTML += '</div>';
    }

    // Footer nav with continue button
    const continueLabel = resp.is_last ? 'See Results' : 'Next question';
    const footerHTML = `
      <div class="msl-footnav">
        <a class="msl-btn msl-btn-ghost"
           href="${resp.next_url.replace(/quiz\/\d+|results/, getQuizUrl())}">
          Retry this question
        </a>
        <a class="msl-btn msl-btn-primary" href="${resp.next_url}">
          ${continueLabel} &rsaquo;
        </a>
      </div>`;

    $main.html(bannerHTML + '<div class="container-fluid mt-3">' + bodyHTML + '</div>');
    $('#msl-footnav-slot').html(footerHTML);
  }

  // Quiz URL of the current question (for "Retry" button)
  function getQuizUrl() {
    const qNum = parseInt($('#msl-question').data('q-num'), 10);
    return 'quiz/' + qNum;
  }

  function escapeHtml(s) {
    if (s === null || s === undefined) return '';
    return String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }
});
