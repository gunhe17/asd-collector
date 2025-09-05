import { fetcher } from "/templates/common/fetcher.js"
import { paramManager } from "/templates/common/param_manager.js"

/**
 * @Component
 */
class Attention {
    constructor() {
        this.indexes = [3]; // 입력한 index의 해당하는 동영상의 재생 전에 발생함.

        this.attention = document.querySelector(`#attention`);
        this.preloadedAudios = {};
    }

    // common
    async init() {
        const user_id = paramManager.get("user_id");
        
        try {
            const user = await fetcher.getUser(user_id);
            const user_called = user.called;
            
            for (const index of this.indexes) {
                let message;
                
                if (index === 2) {
                    message = user_called + "~! 친구들이 뭐하는지 볼래?";
                } else if (index === 9) {
                    message = user_called + "~! 나 따라서 신나게 춤춰볼까? 잘 할 수 있지~?";
                }
                
                if (message) {
                    const audioBlob = await fetcher.openai(message);
                    const audioUrl = URL.createObjectURL(audioBlob);
                    const audio = new Audio(audioUrl);
                    audio.audioUrl = audioUrl;
                    this.preloadedAudios[index] = audio;
                }
            }
        } catch (error) {
            console.error("Failed to preload attention audios:", error);
        }
    }

    async run(index) {
        fetcher.csv(
            paramManager.get("user_id"),
            new Date(Date.now()).toISOString(),
            "attention-start",
            (0).toString()
        );
        
        this._show();

        if (index === 3) {
            await new Promise(resolve => setTimeout(resolve, 5000));
        } else if (index === 9) {
            await new Promise(resolve => setTimeout(resolve, 1000));
        }
        
        let audio;
        if (this.preloadedAudios[index]) {
            audio = this.preloadedAudios[index];
        } else {
            const user = await this._user();
            audio = await this._fallbackLoadAudio(user.called, index);
        }
        
        const audioClone = audio.cloneNode();
        audioClone.play();

        await new Promise(resolve => setTimeout(resolve, 5000));

        this._hide();
        
        fetcher.csv(
            paramManager.get("user_id"),
            new Date(Date.now()).toISOString(),
            "attention-end",
            (0).toString()
        );
        
        return audioClone;
    }

    // unique
    is_run(index) {
        return this.indexes.includes(index) ? true : false;
    }

    // private
    async _user() {
        const user_id = paramManager.get("user_id");
        const user = await fetcher.getUser(user_id);

        return user
    }

    async _fallbackLoadAudio(name, index) {
        let message;

        // *중요. usecase의 record_duration도 수정할 것.

        if (index === 3) {
            message = name + "~! 친구들이 뭐하는지 볼래?";
        }

        const audioBlob = await fetcher.openai(message);
        const audioUrl = URL.createObjectURL(audioBlob);
        const audio = new Audio(audioUrl);
        
        audio.audioUrl = audioUrl;
        
        return audio;
    }

    _show() {
        this.attention.classList.remove("hidden");
    }

    _hide() {
        this.attention.classList.add("hidden");
    }
}

/**
 * @export
 */
export const attention = new Attention();

/**
 * @event
 */
document.addEventListener('DOMContentLoaded', async() => {
    await attention.init();
});