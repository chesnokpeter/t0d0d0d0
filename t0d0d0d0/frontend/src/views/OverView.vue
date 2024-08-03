<template>
<div class="container">
    <logo class="logo"></logo>
    <menu-comp sel="overview" class="menu"></menu-comp>
    <div class="content">
        
    </div>
</div>
</template>


<script setup>
import Logo from '../components/Logo.vue'
import MenuComp from '../components/MenuComp.vue'
</script>

<style>
#app{
    align-items: center;
}
</style>

<style scoped>
* {
    box-sizing: border-box;
}

.container {
    position: relative;
    margin-top: 150px; 
}

.logo {
    display: block;
    width: 100%; 
    /* height: 100%; */
    margin: 0 auto;
}

.menu {
    position: absolute;
    left: -100px;
}

@media (max-width: 750px) {
    .container {
        margin-top: 0px; 
    }
    .logo {
        width: 100%; 
        position: sticky;
        top: 0;
    }
    .menu {
        position: fixed;
        bottom: 0;
        width: 100%;
        left: 0;
    }

}

</style>