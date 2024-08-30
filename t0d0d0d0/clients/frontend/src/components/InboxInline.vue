<template>
    <div class="inbox-wrapper">
        inbox //
        <div class="inbox"></div>
    </div>
</template>

<script>
import { onMounted } from 'vue';
export default {
    props: {
        inboxs: {
            type: Aray,
            required: true
        }
    },
    setup(props) {
        return {
            inboxs:props.inboxs
        }
    }
} 
</script>


<style scoped>
    .menu{
        display: flex;
        flex-direction: column;
        gap: 20px;
        color: var(--gray-color);
    }
    
    a{
        color: var(--gray-color);
        text-decoration: none;
    }
    .sel {
        background-color: var(--gray-color);
        color: var(--black-color);
    }
    
    .el:hover {
        background-color: var(--gray-color);
        color: var(--black-color);
        }

    .sel:hover{
        background-color: var(--black-color);
        color: var(--gray-color);
    }

</style>