import { fetcher } from "/templates/common/fetcher.js"
import { paramManager } from "/templates/common/param_manager.js"

import { player } from "/templates/capture/component/player/component.js"
import { loading } from "/templates/capture/component/loading/component.js"
import { countdown } from "/templates/capture/component/countdown/component.js"
import { monitor } from "/templates/capture/component/monitor/component.js"


/**
 * @Page
 */
class Page {
    constructor() {
        this.main = document.querySelector(`main`);
        this.videoPlayer = document.querySelector(`video[name="video-player"]`);
    }

    // common
    
    async init() {}

    async run() {
        // loading
        loading.show();

        // record camera
        const video_id = paramManager.get("video_id");
        const user_id = paramManager.get("user_id");
        fetcher.record(video_id, user_id)

        // monitor
        monitor.run();

        // loading
        loading.hide();

        // countdown
        countdown.show(10);

        // wait 10s
        await new Promise(resolve => setTimeout(resolve, 10000));

        // play video
        player.play()
    }

    async stop() {
        player.pause()

        const user_id = paramManager.get("user_id");
        fetcher.stop(user_id);
    }
}

/**
 * @export
 */
export const page = new Page();

/**
 * @window
 */
if (!window.page) {
    window.page = page;
}

/**
 * @event
 */

document.addEventListener('DOMContentLoaded', async() => {
    await page.init();
});

let spaceCooldown = false;

document.addEventListener("keydown", async (event) => {
    if (!player.is_checked) return;

    if (
        [
            'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12',
            'Tab', 'Enter', 'Escape', 'Backspace', 'Delete', 'Insert', 'Home', 'End', 'PageUp', 'PageDown', 'PrintScreen', 'ScrollLock', 'Pause'
        ].includes(event.code)
    ) {
        event.preventDefault();
        event.stopPropagation();
        return false;
    }

    /**
     * KEYS
     */

    if (
        event.ctrlKey && 
        event.shiftKey && 
        event.altKey &&
        event.code === "Space" &&
        !event.repeat
    ) {
        // cooldown
        if (spaceCooldown) return;
        spaceCooldown = true; setTimeout(() => spaceCooldown = false, 10000);

        event.preventDefault();

        if (player.current_player.paused) await page.run(); else await page.stop();
    }

    else if (
        event.ctrlKey && 
        event.shiftKey && 
        event.altKey &&
        event.code.startsWith("Digit") &&
        !event.repeat
    ) {
        if (!player.current_player.paused) return;
        
        event.preventDefault();

        window.location.href = `/capture/u/${paramManager.get("user_id")}/v/${event.code.slice("Digit".length)}`;
    }

    else {
        event.preventDefault();
        event.stopPropagation();
        return false;
    }
});