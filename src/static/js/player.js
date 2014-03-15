(function($) {
  soundManager.setup({
    url: kishore_static_root + "/swf/",
    preferFlash: false,
    onready: function() {
      $("body").trigger("soundManager.ready");
    }
  });

  var kishorePlayer = function(element, options) {
    this.$elem = $(element);
    this.options = options;
    this.init();
  }

  kishorePlayer.prototype = {
    init: function() {
      var self = this;
      $("body").on("soundManager.ready", function() {
        self.getSounds();
        self.bindEvents();
      });

      self.play_button = $("input[name=play]");
      self.pause_button = $("input[name=pause]");
      self.seeker = $("input[type=range]");
      self.seeker_timeout = null;
      self.dragging = false;
    },

    // event handlers

    events: {
      play: function() {
        $(this._data.li).addClass("playing");
      },

      stop: function() {
        $(this._data.li).removeClass("playing paused");
      },

      pause: function() {
        var $li = $(this._data.li);
        if (!$li.hasClass("dragging")) {
          $li.addClass("paused");
        }
      },

      resume: function() {
        $(this._data.li).removeClass("paused");
      },

      finish: function() {
        $(this._data.li).removeClass("playing");
      },

      whileloading: function() {
      },

      onload: function() {
      },

      whileplaying: function() {
        var $li = $(this._data.li);
        if (!$li.hasClass("dragging")) {
          var value = this.position/this.durationEstimate*100;
          $(".progress-bar").width(String(value) + "%");
        }
      }
    },

    getSounds: function() {
    },

    getSoundId: function(li) {
      var index = $(this.options.selector + " li").index(li);
      return "sound_" + $(li).attr("data-song-id") + "_" + index;
    },

    bindEvents: function() {
      var self = this;

      $("li", self.$elem).on("click", function(e) {
        e.preventDefault();

        var id = self.getSoundId(this);
        var sound = soundManager.getSoundById(id);

        if (sound) {
          if (sound === self.lastSound) {
            if (sound.readyState !== 2) { // no error
              if (sound.playState !== 1) {
                // not playing
                sound.play();
              } else {
                sound.togglePause();
              }
            }
          } else {
            // different sound
            if (self.lastSound) {
              soundManager.stop(self.lastSound.id);
            }
            sound.togglePause(); // start playing current
          }

        } else {

          // create the sound
          sound = soundManager.createSound({
            id:id,
            url: $(this).attr("data-stream-url"),
            onplay:self.events.play,
            onstop:self.events.stop,
            onpause:self.events.pause,
            onresume:self.events.resume,
            onfinish:self.events.finish,
            whileloading:self.events.whileloading,
            whileplaying:self.events.whileplaying,
            onload:self.events.onload
          });

          sound._data = {li: this};

          // add the controls
          self.createControls(sound);

          if (self.lastSound) soundManager.stop(self.lastSound.id);
          sound.play();

        }

        self.lastSound = sound;
      });

      // self.play_button.on("click", function() {

      //   self.sound = soundManager.createSound({
      //     url: $("li").attr("data-stream-url")
      //   });
      //   self.sound.play({
      //     whileplaying: function() {
      //       if (!self.dragging) {
      //         self.seeker.val(Math.round(self.sound.position/self.sound.durationEstimate*1000));
      //       }
      //     }
      //   });
      // });
      // self.pause_button.on("click", function() {
      //   self.sound.togglePause();
      // });

      // self.seeker.on("change", function(e) {
      //   window.clearTimeout(self.seeker_timeout);
      //   self.sound.pause();
      //   self.dragging = true;
      //   console.log(self.sound.buffered);
      //   self.seeker_timeout = window.setTimeout(function() {
      //     var position = self.seeker.val() / 1000 * self.sound.durationEstimate;
      //     position = Math.min(Math.floor(position), self.sound.duration)
      //     if (!isNaN(position)) {
      //       console.log(position, self.sound.duration);
      //       self.sound.setPosition(position);
      //       self.sound.play();
      //       self.dragging = false;
      //     }
      //   }, 100);
      // });
    },

    getControls: function() {
      var position = '<div class="progress"><div class="progress-bar"></div></div>',
      time = '<span class="song-time"></span>';
      return $('<div class="song-controls">').append(position + time);
    },

    createControls: function(sound) {
      var self = this, $li = $(sound._data.li);

      var position = '<div class="progress"><div class="progress-bar"></div></div>',
      time = '<span class="song-time"></span>',
      controls = $('<div class="song-controls">').append(position + time);

      $li.append(controls);
      $progress = $(".progress", $li);

      function updateposition(e) {
        var value = (e.pageX - $progress.offset().left) / $progress.width() * 100;
        $(".progress-bar", $li).width(String(value) + "%");
      };

      function startdrag(e) {
        e.stopPropagation();
        $li.addClass("dragging");
        sound.pause();
        updateposition(e);
      };

      function stopdrag(e) {
        e.stopPropagation();
        updateposition(e);

        $li.removeClass("dragging");
        position = $(".progress-bar").width() / $progress.width() * sound.durationEstimate;
        sound.setPosition(Math.round(position));
        sound.resume();
      };

      function drag(e) {
        if ($li.hasClass("dragging")) {
          updateposition(e);
        }
      }

      $progress.on("click", function(e) {
        e.stopPropagation();
      });

      $progress.on("mousedown", startdrag);
      $progress.on("mousemove", drag);
      $progress.on("mouseup", stopdrag);
    }
  }

  $.fn.kishoreAudioPlayer = function(option) {
    var selector = this.selector;
    return this.each(function () {
      var $this = $(this)
      , data = $this.data('kishoreAudioPlayer')
      , options = $.extend({}, $.fn.kishoreAudioPlayer.defaults, typeof option == 'object' && option);

      options['selector'] = selector;
      if (!data) $this.data('kishoreAudioPlayer', (data = new kishorePlayer(this, options)))
      if (typeof(option) == 'string') {
        data[action]();
      }
    });
  }

  $.fn.kishoreAudioPlayer.defaults = {
  }

})(jQuery);
