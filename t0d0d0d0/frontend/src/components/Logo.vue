<template>
    <div class="logo">
        <img src="../assets/logo.svg" alt="">
    </div>
</template>

<script>

</script>

<style scoped>
    img {
            max-width: 100%; 
            height: auto;  
            
        }
    .logo {
        width: 100%; 
        margin: 0 auto;
        display: flex;
        justify-content: center;
    }

    @media (max-width: 750px) {
        .logo{
            position: sticky;
            top: 0;
        }
    }
</style>
