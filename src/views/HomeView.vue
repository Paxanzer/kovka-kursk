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


    
    <div class="carousel-container" id="first-carousel" :class="{ 'is-visible': visibleIds.includes('first-carousel') }">
      <button class="carousel-button prev" @click="prevSlide">&lt;</button>
      <div class="carousel-wrapper" :style="{ transform: `translateX(-${currentIndex * 100}%)` }">
        <div class="carousel-slide" v-for="(slide, index) in slides" :key="index"
             :class="{ 'active': currentIndex === index }">
          <img :src="slide.image" :alt="slide.alt">
          <div class="slide-overlay">
            <h3>{{ slide.title }}</h3>
            <p>{{ slide.description }}</p>
          </div>
        </div>
      </div>
      <button class="carousel-button next" @click="nextSlide">&gt;</button>
      
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
    <p class="txt-big-l" id="gallery-title" :class="{ 'is-visible': visibleIds.includes('gallery-title') }">Фотогалерея магазина</p>
    <div class="carousel-container gallery-carousel" id="gallery-carousel" :class="{ 'is-visible': visibleIds.includes('gallery-carousel') }">
      <button class="carousel-button prev" @click="prevGallerySlide">&lt;</button>
      <div class="carousel-wrapper" :style="{ transform: `translateX(-${galleryIndex * 100}%)` }">
        <div class="carousel-slide" v-for="(slide, index) in gallerySlides" :key="index"
             :class="{ 'active': galleryIndex === index }">
          <img :src="slide.image" :alt="slide.alt">
          <div class="slide-overlay">
            <h3>{{ slide.title }}</h3>
            <p>{{ slide.description }}</p>
          </div>
        </div>
      </div>
      <button class="carousel-button next" @click="nextGallerySlide">&gt;</button>
      
      <div class="carousel-dots">
        <span
          v-for="(slide, index) in gallerySlides"
          :key="index"
          :class="{ 'dot': true, 'active': galleryIndex === index }"
          @click="goToGallerySlide(index)"
        ></span>
      </div>
    </div>
  </div>
  <div class="fr-5">
    <p class="txt-big-m" id="cooperation-title" :class="{ 'is-visible': visibleIds.includes('cooperation-title') }">Сотрудничество</p>
    <p class="txt-small-m" id="cooperation-text" :class="{ 'is-visible': visibleIds.includes('cooperation-text') }">Наша организация приглашает к сотрудничеству компании, работающие на территории Российской Федерации, имеющие опыт продаж кованых элементов для создания и развития дилерской сети.</p>
    <div class="fr-5-1">
      <div class="card5" id="card5-1" :class="{ 'is-visible': visibleIds.includes('card5-1') }">
        <p class="card5txtb">Лучшие</p>
        <p class="card5txts">цены на кованые элементы от производителя</p>
      </div>
      <div class="card5" id="card5-2" :class="{ 'is-visible': visibleIds.includes('card5-2') }">
        <p class="card5txtb">Широкий</p>
        <p class="card5txts">ассортимент продукции в наличии</p>
      </div>
      <div class="card5" id="card5-3" :class="{ 'is-visible': visibleIds.includes('card5-3') }">
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
import gallery1 from '@/assets/carousel/1_3.jpg';
import gallery2 from '@/assets/carousel/1_2.jpg';
import gallery3 from '@/assets/carousel/1_1.jpg';

export default {
  setup() {
    const slide = ref(0);
    return { slide };
  },
  data() {
    return {
      visibleIds: [],
      slides: [
        { 
          image: image1, 
          alt: 'Image 1',
          title: 'Художественная ковка',
          description: 'Уникальные кованые изделия ручной работы'
        },
        { 
          image: image2, 
          alt: 'Image 2',
          title: 'Качество материалов',
          description: 'Используем только высококачественные материалы'
        },
        { 
          image: image3, 
          alt: 'Image 3',
          title: 'Индивидуальный подход',
          description: 'Создаем изделия по вашим эскизам'
        }
      ],
      gallerySlides: [
        {
          image: gallery1,
          alt: 'Галерея 1',
          title: 'Наш магазин',
          description: 'Широкий выбор кованых изделий'
        },
        {
          image: gallery2,
          alt: 'Галерея 2',
          title: 'Выставочный зал',
          description: 'Уникальные образцы работ'
        },
        {
          image: gallery3,
          alt: 'Галерея 3',
          title: 'Производство',
          description: 'Современное оборудование'
        }
      ],
      currentIndex: 0,
      galleryIndex: 0,
      autoPlayInterval: null,
      galleryInterval: null
    }
  },
  methods: {
    goToSlide(index) {
      this.currentIndex = index;
    },
    goToGallerySlide(index) {
      this.galleryIndex = index;
    },
    nextSlide() {
      this.currentIndex = (this.currentIndex + 1) % this.slides.length;
    },
    nextGallerySlide() {
      this.galleryIndex = (this.galleryIndex + 1) % this.gallerySlides.length;
    },
    prevSlide() {
      this.currentIndex = this.currentIndex === 0 
        ? this.slides.length - 1 
        : this.currentIndex - 1;
    },
    prevGallerySlide() {
      this.galleryIndex = this.galleryIndex === 0 
        ? this.gallerySlides.length - 1 
        : this.galleryIndex - 1;
    },
    startAutoPlay() {
      this.autoPlayInterval = setInterval(() => {
        this.nextSlide();
      }, 5000);
      this.galleryInterval = setInterval(() => {
        this.nextGallerySlide();
      }, 6000);
    },
    stopAutoPlay() {
      if (this.autoPlayInterval) {
        clearInterval(this.autoPlayInterval);
      }
      if (this.galleryInterval) {
        clearInterval(this.galleryInterval);
      }
    }
  },
  mounted() {
    const idsToObserve = [
      'fr1-1', 
      'fr-element', 
      'fr-2-txt', 
      'txt-big-r', 
      'txt-small-m', 
      'txt-small-m2',
      'first-carousel',
      'gallery-title',
      'gallery-carousel',
      'cooperation-title',
      'cooperation-text',
      'card5-1',
      'card5-2',
      'card5-3'
    ];
    
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const id = entry.target.id;
            if (!this.visibleIds.includes(id)) {
              this.visibleIds.push(id);
            }
            observer.unobserve(entry.target);
          }
        });
      },
      {
        root: null,
        rootMargin: '0px',
        threshold: 0.1,
      }
    );

    idsToObserve.forEach((id) => {
      const element = document.getElementById(id);
      if (element) {
        observer.observe(element);
      }
    });

    this.startAutoPlay();
  },
  beforeUnmount() {
    this.stopAutoPlay();
  }
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
  position: relative;
  width: 100%;
  max-width: 1200px;
  margin: 2rem auto;
  overflow: hidden;
  border-radius: 12px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
}

.carousel-wrapper {
  display: flex;
  transition: transform 0.5s ease-in-out;
  height: 500px;
}

.carousel-slide {
  flex: 0 0 100%;
  position: relative;
  height: 100%;
}

.carousel-slide img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.slide-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.7));
  color: white;
  padding: 2rem;
  transform: translateY(100%);
  transition: transform 0.3s ease-in-out;
}

.carousel-slide:hover .slide-overlay {
  transform: translateY(0);
}

.slide-overlay h3 {
  margin: 0 0 0.5rem;
  font-size: 1.5rem;
}

.slide-overlay p {
  margin: 0;
  font-size: 1rem;
  opacity: 0.9;
}

.carousel-button {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(255, 255, 255, 0.3);
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  color: white;
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s;
  z-index: 2;
}

.carousel-button:hover {
  background: rgba(255, 255, 255, 0.5);
}

.carousel-button.prev {
  left: 1rem;
}

.carousel-button.next {
  right: 1rem;
}

.carousel-dots {
  position: absolute;
  bottom: 1rem;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 0.5rem;
  z-index: 2;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  transition: background-color 0.3s;
}

.dot.active {
  background: white;
  transform: scale(1.2);
}

/* Галерея */
.fr-4 {
  width: 100%;
  padding: 2rem 1rem;
  text-align: center;
}

.txt-big-l {
  font-size: 2rem;
  margin-bottom: 2rem;
  text-align: center;
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

.gallery-carousel {
  margin: 2rem auto;
  background: rgba(255, 255, 255, 0.05);
}

.gallery-carousel .carousel-slide img {
  object-fit: contain;
  background: rgba(0, 0, 0, 0.3);
}

.gallery-carousel .slide-overlay {
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.8));
}

/* Анимации появления для всех элементов */
.carousel-container, .txt-big-l, .txt-big-m, .card5, .txt-small-m {
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.8s ease-out;
}

#first-carousel {
  transform: translateX(-30px);
}

#gallery-carousel {
  transform: translateX(30px);
}

.card5 {
  transform: translateY(50px);
  transition-delay: 0.2s;
}

#card5-2 {
  transition-delay: 0.4s;
}

#card5-3 {
  transition-delay: 0.6s;
}

.txt-big-l, .txt-big-m {
  transform: translateY(-20px);
}
</style>