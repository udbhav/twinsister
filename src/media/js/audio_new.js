function TSPlayer() {
    var self = this;
    var sm = soundManager;

    this.config = {
        flashVersion: 8,
        debugMode: false,
        swfUrl: '/media/js/soundmanager/swf/'
    }

    sm.flashVersion = this.config.flashVersion;
    sm.debugMode = this.config.debugMode;
    sm.url = this.config.swfUrl

    this.handleClick = function(sound_li) {
        var sound = $.data(sound_li, 'sound');

        if (sound == self.lastSound) {

            sound.togglePause();
            if ($(sound_li).hasClass('playing')) {
                $(sound_li).addClass('paused').removeClass('playing');
            } else {
                $(sound_li).addClass('playing').removeClass('paused');
            }

        } else {

            if (self.lastSound) {
                self.lastSound.stop();
                $(".playlist .playing, .playlist .paused").removeClass("playing paused");
            }

            self.lastSound = sound;

            $(sound_li).addClass("playing");

            sound.play({
                whileplaying: function() {
                    console.log(this.position);
                }
            });

        }
    }

    this.init = function() {
        sm._writeDebug('TSPlayer.init()');

        var songs = new Array();
        $(".playlist li").each(function() {
            songs.push($(this).attr("data-song-id"));
        });

        json_string = JSON.stringify(songs);

        $.post("/music/songs/play/", {'data': json_string}, function(data) {
            for (var key in data) {
                $('.playlist li[data-song-id="' + key + '"]').each(function() {
                    $.data(this, 'play_url', data[key]);
                });
            }

            var i = 0;
            $(".playlist li").each(function() {
                var id = 'ts_sound_' + i;
                var sound = sm.createSound({
                    id: id,
                    url: $.data(this, 'play_url')
                });
                $.data(this, 'sound', sound);
                $.data(this, 'sound_id', id);
                i++;
            });

            $(".playlist li").bind("click", function() {
                self.handleClick(this);
            });

        }, "json");

    }

}

var tsPlayer = new TSPlayer();

$(document).ready(function() {
    soundManager.onready(function() {
        if (soundManager.supported()) {
            tsPlayer.init();
        }
    });
});