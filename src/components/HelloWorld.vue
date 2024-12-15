<template>
  <div class="bg-header">
    <div class="flavour-text">Welcome to the F1 Shop</div>
  </div>
</template>

<script>
export default {
  name: "HelloWorld",
};
</script>

<style scoped>
* {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  padding: 0;
  margin: 0;
  box-sizing: border-box;
}

.bg-header {
  position: relative;
  background-image: url("../assets/f1-bg.png");
  background-size: cover;
  background-position: center;
  height: 600px;
  width: auto;
  overflow: hidden;
}

.bg-header::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5); /* Black shadow overlay with 50% opacity */
  z-index: 1; /* Ensure it appears above the background image */
}

.flavour-text {
  position: absolute;
  left: 50px; /* Move text to the right */
  top: 50%; /* Center vertically */
  transform: translateY(-50%); /* Adjust vertical alignment */
  color: rgb(255, 255, 255);
  font-size: 48px; /* Bigger text */
  font-weight: bold;
  text-align: right; /* Align text to the right */
  z-index: 2;
}
</style>
