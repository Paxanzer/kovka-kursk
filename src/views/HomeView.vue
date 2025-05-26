<template>
  <div class="body1">
    
  
  
  <div class="fr_1">

  <div class="fr1-1" id="fr1-1" :class="{ 'is-visible': visibleIds.includes('fr1-1') }">
      <p class="txt1">Элементы художественной ковки</p>
      <p class="sec_txt">Склад-магазин - г.Курск</p>
  </div>
  <!-- пример
    <div class="fr1-1" id="fr1-2" :class="{ 'is-visible': visibleIds.includes('fr1-2') }">
      <p class="txt1">Элементы художественной ковки</p>
      <p class="sec_txt">Склад-магазин - г.Курск</p>
    </div>
    -->
  
    
    <div class="fr-elements" >
      <div class="fr-element" id="fr-element" :class="{ 'is-visible': visibleIds.includes('fr-element') }" >
        <p class="txt-element">Гарантия качества товара</p>
      </div>
      <div class="fr-element" id="fr-element" :class="{ 'is-visible': visibleIds.includes('fr-element') }">
        <p class="txt-element">Лучшие цены в Регионе</p>
      </div>
      <div class="fr-element" id="fr-element" :class="{ 'is-visible': visibleIds.includes('fr-element') }">
        <p class="txt-element">Работаем 7 дней в неделю</p>
      </div>
      <div class="fr-element" id="fr-element" :class="{ 'is-visible': visibleIds.includes('fr-element') }">
        <p class="txt-element">Собственное производство</p>
      </div>
    

      
    </div>
  </div>
  <div class="fr-2" >
    <p class="fr-2-txt" id="fr-2-txt" :class="{ 'is-visible': visibleIds.includes('fr-2-txt') }">ПРИДУМАТЬ ДИЗАЙН Ковка - распространенный способ художественной обработки металла. История ковки и кованых изделий насчитывает тысячи лет, однако в настоящее время наблюдается повышенной спрос на эту продукцию. И это неспроста. Ведь ковка - это долговечность, надежность и прочность. Кованые элементы - это огромные декоративные возможности для создония кованых композиций. Кроме того, художественная ковка отлично сочетается с любым архитектурным стилем и материалом. При производстве кованых изделий наши мастера-кузнецы используют как проверенные временем приемы ручной художественной ковки, так и современные технологии холодной механической ковки . Технологии художественной ковки и изготовления конструкций из стали, позволяют нам оформить интерьер и фасад объектов как в старинном стиле с использованием кованых элементов и натурального дерева. Готовые кованые изделия могут использоваться повсеместно. Использование кованых изделий позволяет создавать атмосферу неповторимого уюта и красоты. Благодаря использованию кованых элементов можно придать эстетически привлекательный вид даже самой простой металлической конструкции начиная от забора и заканчивая оконными решетками. Кованые изделия прекрасно гармонируют с любым стилем оформления. По вашему заказу мы изготовим любое кованое изделие именно тех размеров, которые вам требуются. Также вы можите приобрести кованные элементы в Курске и самостоятельно изготовить любое изделие самостоятельно, либо воспользоваться услугами сварщиков.</p>
  </div>
  <div class="fr-3">
    <p class="txt-big-r" id="txt-big-r" :class="{ 'is-visible': visibleIds.includes('txt-big-r') }">Примеры применения</p>
    <p class="txt-small-m">Благодаря большому ассортименту готовых кованых элементов отечественного и зарубежного производства художественная ковка стала дешевле, художественная ковка стала доступней. Имея начальные навыки кузнечного ремесла и художественный вкус, кованые элементы позволяют создавать оригинальные и неповторимые по красоте кованые изделия.</p>


    
    <div class="carousel-container">
    <div class="carousel-wrapper" :style="{ transform: `translateX(-${currentIndex * 100}%)` }">
      <div class="carousel-slide" v-for="(slide, index) in slides" :key="index">
        <img :src="slide.image" :alt="slide.alt">
      </div>
    </div>

    <div class="carousel-dots">
      <span
        v-for="(slide, index) in slides"
        :key="index"
        :class="{ 'dot': true, 'active': currentIndex === index }"
        @click="goToSlide(index)"
      ></span>
    </div>
  </div>



  



    
    <div class="fr-3-2">
      <p class="txt-small-m" id="txt-small-m" :class="{ 'is-visible': visibleIds.includes('txt-small-m') }" >Применение штампованых и литых элементов в изготовлении кованых изделий значительно снижает себестоимость продукции, сокращает сроки изготовления без потери качества. Современные изделия художественной ковки - кованые ограды, заборы, решетки на окна, собираются из готовых кованых элементов с использованием незначительной ручной обработки и сварки.</p>
      <p class="txt-small-m2" id="txt-small-m2" :class="{ 'is-visible': visibleIds.includes('txt-small-m2') }" >Широкая номенклатура готовых элементов позволяет создавать эксклюзивные изделия и шедевры художественной ковки. Большинство кованых элементов (кованые листья, цветы, виноград ...) уже изготовлены и мастеру-кузнецу остается только ручная ковка оригинальных элементов, а так-же сборка готового изделия.</p>
    </div>
  </div>
  <div class="fr-4">
    <p class="txt-big-l">Фотогалерея магазина</p>
    <div class="fff2"></div>
  </div>
  <div class="fr-5">
    <p class="txt-big-m">Сотрудничество</p>
    <p class="txt-small-m">Наша организация приглашает к сотрудничеству компании, работающие на территории Российской Федерации, имеющие опыт продаж кованых элементов для создания и развития дилерской сети.</p>
    <div class="fr-5-1">
      <div class="card5">
        <p class="card5txtb">Лучшие</p>
        <p class="card5txts">цены на кованые элементы от производителя</p>
      </div>
      <div class="card5">
        <p class="card5txtb">Широкий</p>
        <p class="card5txts">ассортимент продукции в наличии</p>
      </div>
      <div class="card5">
        <p class="card5txtb">Возможность</p>
        <p class="card5txts">заказа любым удобным способом</p>
      </div>
    </div>
  </div>





</div>

</template>

<script>
  import { ref } from 'vue';
  import image1 from '@/assets/carousel/1_1.jpg';
  import image2 from '@/assets/carousel/1_2.jpg'; 
  import image3 from '@/assets/carousel/1_3.jpg'; 

  import { onMounted } from 'vue'; // Импортируем onMounted



  export default {
  setup() {
    const slide = ref(0); // Инициализация через ref для Vue 3
    onMounted(() => {
      // Инициализация карусели может потребоваться для корректной работы.
      // Обычно достаточно самого факта монтирования компонента.
    });
    
    return{
      slide
    };
  },
  data() {
    return {
      
      visibleIds: [], // Массив ID видимых элементов

      slides: [
     { image: image1, alt: 'Image 1' },
     { image: image2, alt: 'Image 2' },
     { image: image3, alt: 'Image 3' }
   ],
      currentIndex: 0,
      
    
    }
    
  },
  methods: {
    goToSlide(index) {
      this.currentIndex = index;
    }
  },

  
  mounted() {
    const idsToObserve = ['fr1-1', 'fr-element', 'fr-2-txt', 'txt-big-r', 'txt-small-m', 'txt-small-m2', /* ... добавьте остальные ID в нужном порядке ... */];

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const id = entry.target.id;
            if (!this.visibleIds.includes(id)) {
              this.visibleIds.push(id); // Добавляем ID в массив видимых элементов
            }
            observer.unobserve(entry.target); // Прекращаем наблюдение после появления
          }
        });
      },
      {
        root: null, // Используем viewport
        rootMargin: '0px',
        threshold: 0.1,
      }
    );

    idsToObserve.forEach((id) => {
      const element = document.getElementById(id);
      if (element) {
        observer.observe(element);
      } else {
        console.warn(`Элемент с id "${id}" не найден.`);
      }
    });
  },
}

</script>

<style scoped>
.body1 {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #1C1A1C;
  color: #FFFFFF;
  font-family: 'Manrope', sans-serif;
  padding: 0;
}

/* Общие стили текста */
.txt1, .sec_txt, .txt-element, 
.fr-2-txt, .txt-big-r, .txt-small-m,
.txt-big-l, .txt-big-m, .card5txtb {
  margin: 0;
  line-height: 1.2;
  transition: all 0.5s ease-out;
}

/* Анимации появления */
.is-visible {
  opacity: 1 !important;
  transform: none !important;
}

/* Первый блок */
.fr_1 {
  width: 100%;
  min-height: 400px;
  padding: 2rem 1rem;
  background-image: url('@/assets/m_img.png');
  background-size: cover;
  background-position: center;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  align-items: center;
}

.fr1-1 {
  max-width: 800px;
  margin-bottom: 2rem;
  opacity: 0;
  transform: translateX(-40px);
}

.txt1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.sec_txt {
  font-size: 1.5rem;
  opacity: 0.65;
}

/* Элементы преимуществ */
.fr-elements {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  width: 90%;
  max-width: 1000px;
  margin: 1rem auto;
}

.fr-element {
  background: rgba(255,255,255,0.1);
  padding: 1rem;
  border-radius: 8px;
  opacity: 0;
  transform: translateY(10px);
}

.txt-element {
  font-size: 1.2rem;
}

/* Текстовый блок */
.fr-2 {
  width: 100%;
  padding: 2rem 1rem;
  max-width: 800px;
  margin: 0 auto;
}

.fr-2-txt {
  font-size: 1rem;
  line-height: 1.5;
  opacity: 0;
  transform: translateY(20px);
}

/* Блок с примерами */
.fr-3 {
  width: 100%;
  padding: 2rem 1rem;
  text-align: center;
}

.txt-big-r {
  font-size: 2rem;
  margin-bottom: 1rem;
  opacity: 0;
  transform: translateX(-40px);
}

.txt-small-m {
  font-size: 1rem;
  opacity: 0.7;
  margin-bottom: 2rem;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

/* Карусель */
.carousel-container {
  width: 100%;
  max-width: 600px;
  margin: 2rem auto;
  position: relative;
}

.carousel-slide img {
  width: 100%;
  height: auto;
  border-radius: 8px;
}

.carousel-dots {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 1rem;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: rgba(255,255,255,0.3);
  cursor: pointer;
}

.dot.active {
  background: rgba(255,255,255,0.8);
}

/* Галерея */
.fr-4 {
  width: 100%;
  padding: 2rem 1rem;
  text-align: right;
}

.txt-big-l {
  font-size: 2rem;
  margin-bottom: 1rem;
  max-width: 800px;
  margin-left: auto;
}

/* Сотрудничество */
.fr-5 {
  width: 100%;
  padding: 2rem 1rem;
  text-align: center;
}

.txt-big-m {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.fr-5-1 {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  max-width: 1000px;
  margin: 2rem auto;
}

.card5 {
  background: rgba(255,255,255,0.1);
  padding: 1.5rem;
  border-radius: 8px;
}

.card5txtb {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.card5txts {
  font-size: 1rem;
  opacity: 0.8;
}

/* Границы разделов */
.fr-2, .fr-3, .fr-4, .fr-5 {
  border-top: 1px solid rgba(189, 189, 189, 0.32);
}

/* Адаптивность */
@media (max-width: 768px) {
  .txt1 { font-size: 2rem; }
  .sec_txt { font-size: 1.2rem; }
  .txt-big-r, .txt-big-l, .txt-big-m { font-size: 1.5rem; }
  .fr-elements { grid-template-columns: 1fr 1fr; }
}

@media (max-width: 480px) {
  .fr-elements { grid-template-columns: 1fr; }
  .txt1 { font-size: 1.8rem; }
}
</style>