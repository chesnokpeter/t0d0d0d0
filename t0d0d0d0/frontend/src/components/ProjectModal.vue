<template>
    <div class="blur" @click="close"></div>
    <div class="modal">
        <div class="label">name</div>
        <input type="text" v-model="nname" class="opt" @input="onInputName" />

        <input type="button" class="opt delete" value="delete" @click="deleteTask"/>
    </div>
</template>

<script>
import { defineComponent, ref, onMounted } from 'vue';
import { request } from '@/modules/requester'

export default defineComponent({

    name: 'ProjectModal',
    emits: ['close'],
    props: {
        id: {
            type: Number,
            required: true,
        },
        name: {
            type: String,
            required: true,
        },
    },

    setup(props, { emit }) {
        const close = () => { emit('close') }
        let inputTimeout = null;
        const nname = ref(props.name)

        onMounted(async ()=> {

        })


        async function editProject(name) {
            await request("/project/edit/name", 'PATCH', {id:props.id, name:name}, true)
            
        }


        async function onInputName() {
            if (inputTimeout) {
                clearTimeout(inputTimeout);
            }
            inputTimeout = setTimeout(async () => {
                await editProject(nname.value)
            }, 300);
        }

        async function deleteTask() {
            await request('/project/delete', 'DELETE', {id:props.id})
            emit('close')
        }


        return { close, onInputName,  deleteTask, nname };
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

.delete {
    border: var(--red-color) solid 1px;
    text-align: center;
}

.delete:hover{
    background-color: var(--red-color);
    color: var(--black-color);
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
/* input[type="button"] {
    text-align: start;
} */

</style>