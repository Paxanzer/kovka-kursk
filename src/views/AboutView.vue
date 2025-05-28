<template>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

    
      <div class="fr_razdel">


        <CategoriesComp />
        


      </div>

    

</template>

<script setup>
import CategoriesComp from '@/components/CategoriesComp.vue';

</script>

<style scoped>

.catalog-container {
  
  display: inline-block;
}
.catalog_txt {
      position: absolute;
    width: 87px;
    height: 39px;
    left: 370px;
    top: 20px;
    font-family: Manrope;
    font-style: normal;
    font-weight: 400;
    font-size: 15px;
    line-height: 22px;
    display: flex
;
    align-items: center;
    color: #FFFFFF;
    opacity: 0;
    transform: translateX(-10px);
    transition: transform 0.4s ease, opacity 0.2s ease;
    pointer-events: none;
    z-index: 0;
  

    
}

.catalog-container:hover .catalog_txt {
  opacity: 0.75;
  transform: translateX(0);
}
.catalog_img {
  position: absolute;
  width: 40px;
  height: 40px;
  left: 323px;
  top: 19px;
  opacity: 0.4;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
  z-index: 2;
}

.catalog_img:hover {
  opacity: 0.75;
}


.card_img {
  width: 215.41px;
  height: 149px;
  left: 0px;
  top: 0px;
  object-fit: cover;
  margin-left: -1px;
  transition: transform 0.3s ease; /* Добавил для плавности */
}

.card_img_fr {
  box-sizing: border-box;
  width: 220px;
  height: 138px;
  left: 0.5px;
  top: 0px;
  border: 4px solid #737373;
  border-radius: 6px;
  margin-top: -4px;
  margin-left: -4px;
  overflow: hidden;
  transition: box-shadow 0.3s ease; /* Анимация для тени */
}

.card_txt {
  width: 248px;
  height: 138px;
  left: 220.5px;
  top: 0px;
  font-family: 'Manrope', sans-serif;
  font-style: normal;
  font-weight: 400;
  font-size: 30px;
  line-height: 36px;
  display: flex;
  align-items: center;
  text-align: center;
  color: #DEDEDE;
  margin-top: -4px;
  transition: text-shadow 0.3s ease; /* Анимация для тени текста */
}

.card_fr {
  display: flex;
  box-sizing: border-box;
  width: 468px;
  height: 138px;
  background: rgba(0, 0, 0, 0.23);
  border: 4px solid #737373;
  border-radius: 6px;
  flex: none;
  order: 0;
  flex-grow: 0;
  cursor: pointer;
  transition: all 0.3s ease; /* Объединил все переходы */
}

.card_fr:hover {
  scale: 1.02;
  box-shadow: 0 8px 24px rgba(222, 222, 222, 0.2); /* Тень при наведении */
}

.card_fr:hover .card_img_fr {
  box-shadow: 0 4px 12px rgba(222, 222, 222, 0.1); /* Тень для изображения */
}

.card_fr:hover .card_txt {
  text-shadow: 0 0 8px rgba(222, 222, 222, 0.4); /* Свечение текста */
}

.card_fr:hover .card_img {
  transform: scale(1.03); /* Легкое увеличение изображения */
}

.fr_razdel{
    box-sizing: border-box;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: center;
    align-items: flex-start;
    align-content: flex-start;
    padding: 45px 33px 28px;
    gap: 47px;
    
    height: 1146px;
    border-top: 1px solid rgba(189, 189, 189, 0.32);
    flex: none;
    order: 1;
    align-self: stretch;
    flex-grow: 0;
}
.search_Btxt{
  position: absolute;
  width: 70px;
  height: 25px;
  left: 21px;
  top: 4px;

  font-family: Manrope;
  font-style: normal;
  font-weight: 400;
  font-size: 24px;
  line-height: 29px;

  color: #1C1A1C;

  font-weight: 700;

  cursor: pointer;
}


.search_input1 {
  box-sizing: border-box;
  position: absolute;
  width: 477px;
  height: 40px;
  left: 0px;
  top: 0px;
  
  background: #1C1A1C;
  border: 2px solid #737373;
  border-radius: 6px;
  color: #DEDEDE;  /* Исправлено с colortxt на color */
  font-size: 24px;
  font-family: Manrope;
  
  /* Дополнительные стили для улучшения вида input */
  padding: 8px 12px;
  outline: none;
  transition: border-color 0.3s ease;
}

/* Стиль для плейсхолдера */
.search_input1::placeholder {
  color: #737373;
  opacity: 1; /* Для Firefox */
}

/* Стиль при фокусе */
.search_input1:focus {
  border-color: #dededeb2;
}
.search_input1:hover {
  border-color: #dededeb2;
}


.search_button{
    box-sizing: border-box;
    position: absolute;
    width: 104px;
    height: 40px;
    left: 465px;
    top: 0px;
    background: #737373;
    border: 1px solid #737373;
    border-radius: 7px;
    cursor: pointer;

}
.search_fr{
    position: absolute;
    width: 571px;
    height: 40px;
    left: 459px;
    top: 19px;
}
.navbar{
    box-sizing: border-box;

    width: 1440px;
    height: 77px;

    border-bottom: 1px solid rgba(189, 189, 189, 0.32);

    /* Inside auto layout */
    flex: none;
    order: 0;
    align-self: stretch;
    flex-grow: 0;
}
.body2{
    /* Auto layout */
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 0px;

    position: relative;
    width: 1440px;
    height: 1223px;

    background: #1C1A1C;
}

.about-title {
  font-family: 'Manrope', sans-serif;
}

.about-text {
  font-family: 'Manrope', sans-serif;
}

.about-text-2 {
  font-family: 'Manrope', sans-serif;
}

</style>
