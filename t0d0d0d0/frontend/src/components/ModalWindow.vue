<template>
    <div class="blur" @click="close"></div>
    <div class="modal">
        <div class="label">name</div>
        <input type="text" v-model="nname" class="opt" @input="onInput" />
        <div class="label">project</div>
        <input type="text" v-model="nproject" class="opt" @input="onInput" />
        <div class="label">date</div>
        <input id="datepic" type="text" v-model="ndate" class="opt" @input="onInput" />
        <div class="label">time</div>
        <!-- <div class="time">
            <input type="number" class="time-hours" @input="onInput" v-model="nhours">
            :
            <input type="number" class="time-minutes" @input="onInput" v-model="nminutes">
            :
            <input type="number" class="time-seconds" @input="onInput" v-model="nseconds">
        </div> -->
        <!-- <input type="time" step=1 v-model="ntime" class="opt"@input="onInput" /> -->
        <vue-timepicker format="hh:mm:ss" hide-clear-button></vue-timepicker>
    </div>
</template>

<script>
import { defineComponent, ref,  } from 'vue';
import { useDatepicker } from 'vue-air-datepicker'
import localeEn from 'air-datepicker/locale/en';
import 'air-datepicker/air-datepicker.css';
import '@/assets/custom_airdatepicker.css'

import VueTimePicker from "vue3-timepicker";
import "vue3-timepicker/dist/VueTimepicker.css";

export default defineComponent({
    components: {
        "vue-timepicker": VueTimePicker,
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
            type: String,
            required: false,
        },
        date: {
            type: String,
            required: false,
        },
        time: {
            type: String,
            required: false,
        },
    },

    setup(props, { emit }) {
        const close = () => { emit('close') }
        let inputTimeout = null;
        function onInput() {
            if (inputTimeout) {
                clearTimeout(inputTimeout);
            }

            inputTimeout = setTimeout(() => {
                console.log(nname);
            }, 1000);
        }

        const nname = ref(props.name)
        const nproject = ref(props.project)
        const ndate = ref(props.date)
        const ntime = ref(props.time)

        // const nhours = ntime.value.split(':')[0]
        // const nminutes = ntime.value.split(':')[1]
        // const nseconds = ntime.value.split(':')[2]

        useDatepicker('#datepic',{
            selectedDates: [ndate.value],
            isMobile:true,
            locale: localeEn,
            dateFormat: 'yyyy-MM-dd',
            onSelect(date){
                console.log(date);
            }
            // inline: true,
        })
        return { close, onInput, nname, nproject, ndate, ntime,  };
    },
});
</script>

<style scoped>

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