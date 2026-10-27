// ResumeForge AI Client Utilities

document.addEventListener('DOMContentLoaded', function () {
  // Auto-dismiss alerts after 5 seconds
  const alerts = document.querySelectorAll('.alert-dismissible');
  alerts.forEach(function (alert) {
    setTimeout(function () {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      if (bsAlert) bsAlert.close();
    }, 5000);
  });

  // Preset role selector auto-fill
  const presetSelect = document.getElementById('presetRoleSelect');
  const jobTitleInput = document.getElementById('jobTitleInput');
  if (presetSelect && jobTitleInput) {
    presetSelect.addEventListener('change', function () {
      if (this.value) {
        jobTitleInput.value = this.value;
      }
    });
  }

  // Wizard preset role selector
  const wizardSelect = document.getElementById('wizardPresetSelect');
  const customTarget = document.querySelector('input[name="custom_target_role"]');
  if (wizardSelect && customTarget) {
    wizardSelect.addEventListener('change', function () {
      if (this.value) {
        customTarget.value = this.value;
      }
    });
  }
});

// Single Bullet Point AI Enhancement via AJAX
async function enhanceBulletAjax(bulletId, targetRole, csrfToken) {
  const textarea = document.getElementById(bulletId);
  const btn = document.getElementById('btn_' + bulletId);
  if (!textarea || !textarea.value.trim()) return;

  const originalText = textarea.value;
  if (btn) {
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Enhancing...';
  }

  try {
    const res = await fetch('/builder/api/enhance-bullet/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify({
        bullet_text: originalText,
        target_role: targetRole,
      }),
    });

    const data = await res.json();
    if (data.status === 'success' && data.improved) {
      textarea.value = data.improved;
    } else {
      alert('Could not enhance bullet: ' + (data.message || 'Unknown error'));
    }
  } catch (err) {
    alert('Request failed: ' + err.message);
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.innerHTML = '<i class="bi bi-magic"></i> AI Polish';
    }
  }
}
