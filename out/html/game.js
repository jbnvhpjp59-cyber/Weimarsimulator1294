(function() {
  var game;
  var ui;

  var main = function(dendryUI) {
    ui = dendryUI;
    game = ui.game;

    // When hosted somewhere that hot-reloads the page on an update (such as
    // a claude.ai artifact), keep the game in progress across the reload.
    var hot = window.claude && window.claude.hot;
    if (hot && hot.snapshot) {
      hot.snapshot(function() {
        return {state: JSON.parse(JSON.stringify(ui.dendryEngine.getExportableState()))};
      });
    }
    var restore = function(data) {
      if (data && data.state && data.state.qualities && data.state.qualities.started) {
        try {
          ui.dendryEngine.setState(data.state);
        } catch (e) {
          console.log('Could not restore the game in progress:', e);
        }
      }
    };
    if (hot && hot.ready) {
      hot.ready(restore);
    } else if (hot && hot.data) {
      restore(hot.data);
    }
  };

  // Storage can be unavailable (private windows, blocked site data).
  var readStorage = function(key) {
    try {
      return window.localStorage.getItem(key);
    } catch (e) {
      return null;
    }
  };

  window.showStats = function() {
    if (window.dendryUI.dendryEngine.state.sceneId.startsWith('library')) {
        window.dendryUI.dendryEngine.goToScene('backSpecialScene');
    } else {
        window.dendryUI.dendryEngine.goToScene('library');
    }
  };

  window.updateAudio = function(song) {
      var now_playing = document.getElementById('currently_playing');
      if (song) {
          var a = song.split('/');
          now_playing.textContent = a[a.length-1];
      } else if (window.dendryUI.currentAudioURL) {
          var s = window.dendryUI.currentAudioURL;
          var b = s.split('/');
          now_playing.textContent = b[b.length-1];
      }
  };

  // sets the volume
  window.setVolume = function(volume) {
      if (window.dendryUI.currentAudio) {
          window.dendryUI.volume = volume/100;
          window.dendryUI.currentAudio.volume = volume/100;
      }
  };

  // Play a track for a big moment straight away, then go back to shuffling
  // the current playlist. The track itself is not added to the playlist.
  window.playMoment = function(file) {
      var ui = window.dendryUI;
      if (!ui || ui.disable_audio) {
          return;
      }
      var playlist = ui.audioPlaylist.slice();
      ui.audio(file);
      ui.audioPlaylist = playlist;
      var audio = ui.currentAudio;
      if (!audio) {
          return;
      }
      audio.onended = function() {
          var pool = ui.audioPlaylist;
          if (!pool.length) {
              return;
          }
          var next = pool[Math.floor(Math.random() * pool.length)];
          audio.src = next;
          ui.currentAudioURL = next;
          audio.play();
          window.updateAudio(next);
      };
  };

  // go to the next song - this just sets the time to 9999.
  window.shuffle = function() {
      if (window.dendryUI.currentAudio) {
          window.dendryUI.currentAudio.currentTime = 9999;
      }
  };

  // toggles pause or play of music
  window.togglePausePlay = function() {
      if (window.dendryUI.currentAudio) {
          if (window.dendryUI.currentAudio.paused) {
            window.dendryUI.currentAudio.play();
            document.getElementById('pause-button-image').style.display = "inline";
            document.getElementById('play-button-image').style.display = "none";
            document.getElementById('pause-button-text').textContent = "Pause";
          } else {
            window.dendryUI.currentAudio.pause();
            document.getElementById('play-button-image').style.display = "inline";
            document.getElementById('pause-button-image').style.display = "none";
            document.getElementById('pause-button-text').textContent = "Play";
          }
      }
  };

  window.showOptions = function() {
      var save_element = document.getElementById('options');
      window.populateOptions();
      save_element.style.display = "block";
      if (!save_element.onclick) {
          save_element.onclick = function(evt) {
              var target = evt.target;
              var save_element = document.getElementById('options');
              if (target == save_element) {
                  window.hideOptions();
              }
          };
      }
  };

  window.hideOptions = function() {
      var save_element = document.getElementById('options');
      save_element.style.display = "none";
  };

  window.disableBg = function() {
      window.dendryUI.disable_bg = true;
      document.body.style.backgroundImage = 'none';
      window.dendryUI.saveSettings();
  };

  window.enableBg = function() {
      window.dendryUI.disable_bg = false;
      window.dendryUI.setBg(window.dendryUI.dendryEngine.state.bg);
      window.dendryUI.saveSettings();
  };

  window.disableAnimate = function() {
      window.dendryUI.animate = false;
      window.dendryUI.saveSettings();
  };

  window.enableAnimate = function() {
      window.dendryUI.animate = true;
      window.dendryUI.saveSettings();
  };

  window.disableAudio = function() {
      window.dendryUI.toggle_audio(false);
      window.dendryUI.saveSettings();
  };

  window.enableAudio = function() {
      window.dendryUI.toggle_audio(true);
      window.dendryUI.saveSettings();
  };

  window.enableImages = function() {
      window.dendryUI.show_portraits = true;
      window.dendryUI.saveSettings();
  };

  window.disableImages = function() {
      window.dendryUI.show_portraits = false;
      window.dendryUI.saveSettings();
  };

  window.enableLightMode = function() {
      window.dendryUI.dark_mode = false;
      document.body.classList.remove('dark-mode');
      window.dendryUI.saveSettings();
  };
  window.enableDarkMode = function() {
      window.dendryUI.dark_mode = true;
      document.body.classList.add('dark-mode');
      window.dendryUI.saveSettings();
  };

  // populates the checkboxes in the options view
  window.populateOptions = function() {
    var disable_bg = window.dendryUI.disable_bg;
    var animate = window.dendryUI.animate;
    var disable_audio = window.dendryUI.disable_audio;
    var show_portraits = window.dendryUI.show_portraits;
    if (disable_bg) {
        $('#backgrounds_no')[0].checked = true;
    } else {
        $('#backgrounds_yes')[0].checked = true;
    }
    if (animate) {
        $('#animate_yes')[0].checked = true;
    } else {
        $('#animate_no')[0].checked = true;
    }
    if (disable_audio) {
        $('#audio_no')[0].checked = true;
    } else {
        $('#audio_yes')[0].checked = true;
    }
    if (show_portraits) {
        $('#images_yes')[0].checked = true;
    } else {
        $('#images_no')[0].checked = true;
    }
    if (window.dendryUI.dark_mode) {
        $('#dark_mode')[0].checked = true;
    } else {
        $('#light_mode')[0].checked = true;
    }
  };

  // This function allows you to modify the text before it's displayed.
  window.displayText = function(text) {
      return text;
  };

  // This function allows you to do something in response to signals.
  window.handleSignal = function(signal, event, scene_id) {
  };

  // This function runs on a new page. Right now, this auto-saves.
  window.onNewPage = function() {
    var scene = window.dendryUI.dendryEngine.state.sceneId;
    if (scene != 'root' && !window.justLoaded) {
        window.dendryUI.autosave();
    }
    if (window.justLoaded) {
        window.justLoaded = false;
    }
  };

  // On phones the status panel folds into a one-line summary above the game.
  var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                'August', 'September', 'October', 'November', 'December'];
  window.updateStatusSummary = function() {
      var el = document.getElementById('status_summary');
      if (!el) {
          return;
      }
      var Q = dendryUI.dendryEngine.state.qualities;
      if (!Q.started) {
          el.textContent = 'Status';
          return;
      }
      var parts = [MONTHS[(Q.month || 1) - 1] + ' ' + Q.year, 'Resources ' + Q.resources];
      if (!Q.historical_mode && Q.con_votes !== undefined) {
          parts.push('Con ' + Number(Q.con_votes).toFixed(1) + '% · Lab ' + Number(Q.lab_votes).toFixed(1) + '%');
      }
      el.textContent = parts.join(' · ');
  };
  window.setStatusOpen = function(open) {
      document.body.classList.toggle('status-open', open);
      var button = document.getElementById('status_toggle');
      if (button) {
          button.setAttribute('aria-expanded', open ? 'true' : 'false');
      }
  };
  window.toggleStatus = function() {
      var open = !document.body.classList.contains('status-open');
      window.setStatusOpen(open);
      try {
          window.localStorage.setItem(window.dendryUI.game.title + '_status_open', open ? '1' : '0');
      } catch (e) {}
  };

  // Tabbed sidebar: each tab renders a section of status.scene.dry.
  window.updateSidebar = function() {
      $('#qualities').empty();
      window.updateStatusSummary();
      // nothing to show until a game has started (e.g. on the title screen)
      if (!dendryUI.dendryEngine.state.qualities.started) {
          $('#qualities').append($('<p>').text('Start a game to see the state of the nation.'));
          return;
      }
      var scene = dendryUI.game.scenes[window.statusTab];
      dendryUI.dendryEngine._runActions(scene.onArrival);
      var displayContent = dendryUI.dendryEngine._makeDisplayContent(scene.content, true);
      $('#qualities').append(dendryUI.contentToHTML.convert(displayContent));
  };

  window.changeTab = function(newTab, tabId) {
      if (tabId == 'poll_tab' && dendryUI.dendryEngine.state.qualities.historical_mode) {
          window.alert('Polls are not available in historical mode.');
          return;
      }
      var tabButton = document.getElementById(tabId);
      var tabButtons = document.getElementsByClassName('tab_button');
      for (var i = 0; i < tabButtons.length; i++) {
        tabButtons[i].className = tabButtons[i].className.replace(' active', '');
      }
      tabButton.className += ' active';
      window.statusTab = newTab;
      window.updateSidebar();
  };

  window.onDisplayContent = function() {
      window.updateSidebar();
  };

  window.justLoaded = true;
  window.statusTab = "status";
  window.dendryModifyUI = main;
  console.log("Modifying stats: see dendryUI.dendryEngine.state.qualities");

  window.increaseFontSize = function() {
        window.dendryUI.font_size += 0.1;
        var fs = window.dendryUI.font_size;
        var sidebar_fs = fs - 0.1;
        document.getElementById("content").setAttribute("style", "font-size: " + fs + "em;");
        document.getElementById("stats_sidebar").setAttribute("style", "font-size: " + sidebar_fs + "em;");
        document.getElementById('font_size_value').textContent = window.dendryUI.font_size.toFixed(1) + "em";
        window.dendryUI.saveSettings();
  };

  window.decreaseFontSize = function() {
        window.dendryUI.font_size -= 0.1;
        var fs = window.dendryUI.font_size;
        var sidebar_fs = fs - 0.1;
        document.getElementById("content").setAttribute("style", "font-size: " + fs + "em;");
        document.getElementById("stats_sidebar").setAttribute("style", "font-size: " + sidebar_fs + "em;");
        document.getElementById('font_size_value').textContent = window.dendryUI.font_size.toFixed(1) + "em";
        window.dendryUI.saveSettings();
  };

  window.onload = function() {
    window.dendryUI.loadSettings({show_portraits: true});
    // With no saved choice, follow the viewer's light or dark theme.
    if (readStorage(window.dendryUI.game.title + '_dark_mode') === null) {
      var theme = document.documentElement.getAttribute('data-theme');
      var prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
      window.dendryUI.dark_mode = theme === 'dark' || (theme !== 'light' && prefersDark);
    }
    if (window.dendryUI.dark_mode) {
        document.body.classList.add('dark-mode');
    }
    // phones: reopen the status panel if the player left it open
    window.setStatusOpen(readStorage(window.dendryUI.game.title + '_status_open') === '1');
    if (window.dendryUI.font_size != 1.1) {
        var fs = window.dendryUI.font_size;
        var sidebar_fs = fs - 0.1;
        document.getElementById("content").setAttribute("style", "font-size: " + fs + "em;");
        document.getElementById("stats_sidebar").setAttribute("style", "font-size: " + sidebar_fs + "em;");
    }
    document.getElementById('font_size_value').textContent = window.dendryUI.font_size.toFixed(1) + "em";
    window.pinnedCardsDescription = "Shadow Cabinet - one advisor action every 6 months.";
  };

}());
