import { fetcher } from "/templates/common/fetcher.js"


/**
 * @Component
 */
class Monitor {
    constructor() {
        this.monitor = document.querySelector(`#monitor`);

        this.realsense_dot = null;
        this.tobii_dot = null;

        this.realsense_count = 0;
        this.tobii_count = 0;
    }

    // common

    init() {
        this.monitor = document.querySelector(`#monitor`);
        this.realsense_dot = this.monitor.querySelector('#realsense');
        this.tobii_dot = this.monitor.querySelector('#tobii');
    }

    async run() {
        setInterval(async () => {
            const monitored = await fetcher.monitor();

            this._realsense(monitored.realsense);
            this._tobii(monitored.tobii);
        }, 5000);
    }

    // unique
    _realsense(count) {
        const diff = count - this.realsense_count;

        if (diff > 15) {
            this._realsense_valid(diff);
        } else {
            this._realsense_invalid();
        }

        this.realsense_count = count;
    }

    _tobii(count) {
        const diff = count - this.tobii_count;

        if (diff > 15) {
            this._tobii_valid();
        } else {
            this._tobii_invalid();
        }

        this.tobii_count = count;
    }

    _realsense_valid() {
        this.realsense_dot.className = 'w-1 h-1 rounded-full bg-green-900 transition-colors duration-300';
    }
    _realsense_invalid() {
        this.realsense_dot.className = 'w-1 h-1 rounded-full bg-red-900 transition-colors duration-300';
    }
    _tobii_valid() {
        this.tobii_dot.className = 'w-1 h-1 rounded-full bg-green-900 transition-colors duration-300';
    }
    _tobii_invalid() {
        this.tobii_dot.className = 'w-1 h-1 rounded-full bg-red-900 transition-colors duration-300';
    }
}

/**
 * @export
 */
export const monitor = new Monitor();

/**
 * @event
 */
document.addEventListener('DOMContentLoaded', async() => {
    monitor.init();
});