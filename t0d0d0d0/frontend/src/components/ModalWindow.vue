<template>
    <div class="blur" @click="close"></div>
    <div class="modal">
        <div class="label">name</div>
        <input type="text" v-model="nname" class="opt" @input="onInputName" />
        <div class="label">project</div>

        <VueSelect
            v-model="nproject"
            :options="projects"
            placeholder="..."
        />

        <input type="text" v-model="nproject" class="opt" @input="onInputProject" />
        <div class="label">date</div>
        <input id="datepic" type="text" v-model="ndate" class="opt" />
        <div class="label">time</div>

        <div class="time">
            <input min="00" max="24" type="number" class="time-hours" @input="onInput" v-model="nhours">
            :
            <input min="00" max="60" type="number" class="time-minutes" @input="onInput" v-model="nminutes">
        </div>
        <!-- <input type="time" step=1 v-model="ntime" class="opt"@input="onInput" /> -->
        <!-- <vue-timepicker format="hh:mm:ss" hide-clear-button></vue-timepicker> -->
    </div>
</template>

<script>
import { defineComponent, ref, onMounted } from 'vue';
import { request } from '@/modules/requester'
import { useDatepicker } from 'vue-air-datepicker'
import localeEn from 'air-datepicker/locale/en';
import VueSelect from "vue3-select-component";
import 'air-datepicker/air-datepicker.css';
import '@/assets/custom_airdatepicker.css'

// import VueTimePicker from "vue3-timepicker";
// import "vue3-timepicker/dist/VueTimepicker.css";

export default defineComponent({
    components: {
        // "vue-timepicker": VueTimePicker,
        "VueSelect":VueSelect
    },
    name: 'ModalWindow',
    emits: ['close'],
    props: {
        kind: {
            type: String,
            required: false,
            default: 'task'
        },
        name: {
            type: String,
            required: false,
        },
        project: {
            type: Number,
            required: false,
        },
        date: {
            type: String,
            required: false,
        },
        time: {
            type: String,
            required: false,
            default: '00:00'
        },
    },

    setup(props, { emit }) {
        const close = () => { emit('close') }
        let inputTimeout = null;

        const nname = ref(props.name)
        const nproject = ref(props.project)
        const ndate = ref(props.date)
        const ntime = ref(props.time)
        if (Boolean(ntime.value) == false) {
            ntime.value = '00:00'
        }
        const nhours = ntime.value.split(':')[0]
        const nminutes = ntime.value.split(':')[1]

        const projects = ref([])
        onMounted(async ()=> {
            let r = await request('/project/get/projects', 'GET', {}, true)
            projects.value = r.data.map(item => ({
                ...item,
                label: item.name,
                value: item.id
            }));
        })


        useDatepicker('#datepic',{
            selectedDates: [ndate.value],
            isMobile:true,
            locale: localeEn,
            dateFormat: 'yyyy-MM-dd',
            autoClose: true,
            onSelect(date){
                console.log(date);
            }
            // inline: true,
        })


        function onInputName() {
            if (inputTimeout) {
                clearTimeout(inputTimeout);
            }
            inputTimeout = setTimeout(() => {
                console.log(nname);
            }, 1000);
        }

        function onInputProject() {
            if (inputTimeout) {
                clearTimeout(inputTimeout);
            }
            inputTimeout = setTimeout(() => {
                console.log(nproject);
            }, 1000);
        }

        function onInputTime() {
            if (inputTimeout) {
                clearTimeout(inputTimeout);
            }
            inputTimeout = setTimeout(() => {
                console.log(ntime);
            }, 1000);
        }

        function onInput() {
            if (inputTimeout) {
                clearTimeout(inputTimeout);
            }
            inputTimeout = setTimeout(() => {
                console.log(nname);
            }, 1000);
        }

        return { close, onInputName, onInputProject, onInputTime, nname, nproject, ndate, ntime, nhours, nminutes, projects  };
    },
});
</script>



<style scoped>

:deep(.vue-select .menu-option) {
    background-color: #3636d2;
}

:root {
    --vs-input-bg: #543131;
    --vs-input-outline: #3b82f6;
    --vs-input-placeholder-color: #52525b;

    --vs-padding: 0.25rem 0.5rem;
    --vs-border: 1px solid #e4e4e7;
    --vs-border-radius: 4px;
    --vs-font-size: 16px;
    --vs-font-weight: 400;
    --vs-font-family: inherit;
    --vs-text-color: #18181b;
    --vs-line-height: 1.5;

    --vs-menu-offset-top: 8px;
    --vs-menu-height: 200px;
    --vs-menu-padding: 0;
    --vs-menu-border: 1px solid #e4e4e7;
    --vs-menu-bg: #fff;
    --vs-menu-box-shadow: none;
    --vs-menu-z-index: 2;

    --vs-option-padding: 8px 12px;
    --vs-option-font-size: var(--vs-font-size);
    --vs-option-font-weight: var(--vs-font-weight);
    --vs-option-text-color: var(--vs-text-color);
    --vs-option-bg: var(--vs-menu-bg);
    --vs-option-hover-color: #dbeafe;
    --vs-option-focused-color: var(--vs-option-hover-color);
    --vs-option-selected-color: #93c5fd;
    --vs-option-disabled-color: #f4f4f5;
    --vs-option-disabled-text-color: #52525b;

    --vs-multi-value-gap: 4px;
    --vs-multi-value-padding: 4px;
    --vs-multi-value-font-size: 14px;
    --vs-multi-value-font-weight: 400;
    --vs-multi-value-line-height: 1;
    --vs-multi-value-text-color: #3f3f46;
    --vs-multi-value-bg: #f4f4f5;
    --vs-multi-value-xmark-size: 16px;
    --vs-multi-value-xmark-color: var(--vs-multi-value-text-color);

    --vs-indicators-gap: 4px;
    --vs-icon-size: 20px;
    --vs-icon-color: var(--vs-text-color);

    --vs-dropdown-transition: transform 0s ease-out;
}


.blur {
    background: rgba(0, 0, 0, 0.5);
    position: fixed;
    height: 100vh;
    width: 100vw;
    top: 0;
    left: 0;
    backdrop-filter: blur(2px);
    z-index: 4;
}

.modal {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: #121212;
    padding: 20px;
    box-shadow: 20px 20px 0px 0px rgba(0, 0, 0, 1);
    border: var(--white-color) solid 1px;
    z-index: 5;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.label {
    color: var(--gray-color);
    font-size: 12px;
}

.opt {
    font-size: 16px;
}

input{
    border-color: none;
    padding: 10px;
    background-color: var(--black-color);
    border: var(--gray-color) solid 1px;
    color: var(--white-color);
    font-family: "Source Code Pro", monospace;
    font-size: 16px;
}

input:hover{
    background-color: var(--gray-color);
    color: var(--black-color);
}   

input:focus, button {
    outline: none;
}
input[type="button"] {
    text-align: start;
}
</style>