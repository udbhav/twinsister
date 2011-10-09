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

    this.padSeconds = function(number) {
        var str = '' + number;
        while (str.length < 2) {
            str = '0' + str;
        }
   
        return str;
    }

    this.getPosition = function(sound) {
        var position = Math.round(sound.position/1000);
        var duration = Math.round(sound.durationEstimate/1000);

        return Math.floor(position/60) + ':' + self.padSeconds(position % 60) + ' / ' + Math.floor(duration/60) + ':' + self.padSeconds(duration % 60);
    }

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

            var controls = '<div id="song_controls"><div id="song_loading"><div id="song_position"></div></div></div>';

            $(sound_li).addClass("playing").append(controls);

            $("#song_controls").click(function(event) {
                event.stopPropagation();
            });

            $("#song_position").draggable({
                axis: "x",
                containment: "#song_controls",
                start: function(event, ui) {
                    sound.pause();
                },
                drag: function(event, ui) {
                    var new_position = Math.round((ui.position.left/$("#song_controls").width()) * sound.durationEstimate / 1000);
                    var duration = Math.round(sound.durationEstimate/1000);
                    var new_time = Math.floor(new_position/60) + ':' + self.padSeconds(new_position % 60) + ' / ' + Math.floor(duration/60) + ':' + self.padSeconds(duration % 60);
                    $("#song_time").html(new_time);
                    
                },
                stop: function(event, ui) {
                    var new_position = Math.round((ui.position.left/$("#song_controls").width()) * sound.durationEstimate);
                    sound.play();
                    sound.setPosition(new_position);
                    $(".playlist .paused").removeClass("paused").addClass("playing");
                }
            });

            $(sound_li).children(".song_extras").append('<div id="song_time"></div>');

            sound.play({
                whileplaying: function() {
                    var left = Math.round(($("#song_controls").width() - $("#song_position").width()) * (sound.position/sound.durationEstimate));
                    $("#song_position").css("left", left);
                    $("#song_time").html(self.getPosition(sound));
                },
                whileloading: function() {
                    $("#song_loading").width(((this.bytesLoaded/this.bytesTotal) * 100) + '%');
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