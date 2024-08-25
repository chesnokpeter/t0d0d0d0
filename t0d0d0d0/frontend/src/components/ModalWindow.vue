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

        <div class="label">date</div>
        <input id="datepic" type="text" v-model="ndate" class="opt" />
        <div class="label">time</div>

        <div class="time">
            <input min="00" max="24" type="number" class="time-hours" @input="onInput" v-model="nhours">
            :
            <input min="00" max="60" type="number" class="time-minutes" @input="onInput" v-model="nminutes">
        </div>

        <div class="label">status</div>
        <VueSelect
            v-model="nstatus"
            :options="[{label:'backlog', value:'backlog'}, {label:'done', value:'done'}, {label:'stop', value:'stop'}]"
            placeholder="..."
        />
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
import '@/assets/custom_vueselect.css'

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
        status: {
            type: String,
            required: false,
            default: 'backlog'
        },
    },

    setup(props, { emit }) {
        const close = () => { emit('close') }
        let inputTimeout = null;

        const nname = ref(props.name)
        const nproject = ref(props.project)
        const ndate = ref(props.date)
        const nstatus = ref(props.status)
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

        return { close, onInputName, onInputProject, onInputTime, nname, nproject, ndate, ntime, nhours, nminutes, nstatus, projects  };
    },
});
</script>



<style scoped>
@import url('@/assets/custom_vueselect.css');

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

.time {
    display: flex;
    align-items: center;
}

.time-minutes, .time-hours{
    flex: 1;
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