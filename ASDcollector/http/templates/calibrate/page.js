import { fetcher } from "/templates/common/fetcher.js"
import { paramManager } from "/templates/common/param_manager.js"


/**
 * @Page
 */
class Page {
    constructor() {
        this.main = document.querySelector(`main`);
    }

    // common
    async init() {   
    }

    // unique
    test() {
        fetcher.calibration_test(paramManager.get('user_id'));
    }

    drop() {
        fetcher.calibration_delete(paramManager.get('user_id'));

        // window.location.href = `/capture/u/${paramManager.get('user_id')}/v/1`;
    }

    use() {
        window.location.href = `/capture/u/${paramManager.get('user_id')}/v/1`;
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