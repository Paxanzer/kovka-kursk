<template>
  <div class="body1">
    
  
  
  <div class="fr_1">
    <div class="contact-info" id="contact-info" :class="{ 'is-visible': visibleIds.includes('contact-info') }">
      <p class="contact-text">
        <a href="tel:+79155189540" class="contact-link">+7 915 518-95-40</a>
      </p>
      <p class="contact-text">
        <a href="mailto:dmitrii-gorbulin@mail.ru" class="contact-link">dmitrii-gorbulin@mail.ru</a>
      </p>
    </div>

    <div class="fr1-1" id="fr1-1" :class="{ 'is-visible': visibleIds.includes('fr1-1') }">
      <p class="txt1">Ковка на дом</p>
      <p class="sec_txt">Склад-магазин - г.Курск</p>
    </div>

    <div class="fr1-1" id="fr1-1" :class="{ 'is-visible': visibleIds.includes('fr1-1') }">
      <p class="sec_txt">пр-кт. Кулакова, Д-1-В</p>
      <p class="sec_txt">Магазин Элементы художественной ковки</p>
    </div>

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
  <div class="fr-2">
    <div class="text-sections">
      <div class="text-section" id="section1" :class="{ 'is-visible': visibleIds.includes('section1') }">
        <h2 class="section-title">История и традиции</h2>
        <p class="section-text">
          Ковка - распространенный способ художественной обработки металла. История ковки и кованых изделий насчитывает тысячи лет, однако в настоящее время наблюдается повышенной спрос на эту продукцию. И это неспроста. Ведь ковка - это долговечность, надежность и прочность.
        </p>
      </div>

      <div class="text-section" id="section2" :class="{ 'is-visible': visibleIds.includes('section2') }">
        <h2 class="section-title">Декоративные возможности</h2>
        <p class="section-text">
          Кованые элементы - это огромные декоративные возможности для создания кованых композиций. Художественная ковка отлично сочетается с любым архитектурным стилем и материалом.
        </p>
      </div>

      <div class="text-section" id="section3" :class="{ 'is-visible': visibleIds.includes('section3') }">
        <h2 class="section-title">Технологии производства</h2>
        <p class="section-text">
          При производстве кованых изделий наши мастера-кузнецы используют как проверенные временем приемы ручной художественной ковки, так и современные технологии холодной механической ковки. Технологии художественной ковки и изготовления конструкций из стали позволяют нам оформить интерьер и фасад объектов в старинном стиле с использованием кованых элементов и натурального дерева.
        </p>
      </div>

      <div class="text-section" id="section4" :class="{ 'is-visible': visibleIds.includes('section4') }">
        <h2 class="section-title">Универсальность применения</h2>
        <p class="section-text">
          Готовые кованые изделия могут использоваться повсеместно. Использование кованых изделий позволяет создавать атмосферу неповторимого уюта и красоты. Благодаря использованию кованых элементов можно придать эстетически привлекательный вид даже самой простой металлической конструкции: от забора до оконных решеток.
        </p>
      </div>

      <div class="text-section" id="section5" :class="{ 'is-visible': visibleIds.includes('section5') }">
        <h2 class="section-title">Индивидуальный подход</h2>
        <p class="section-text">
          Кованые изделия прекрасно гармонируют с любым стилем оформления. По вашему заказу мы изготовим любое кованое изделие именно тех размеров, которые вам требуются. Также вы можете приобрести кованые элементы в Курске и самостоятельно изготовить любое изделие или воспользоваться услугами сварщиков.
        </p>
      </div>
    </div>
  </div>
  <div class="fr-3">
    <p class="txt-big-r" id="txt-big-r" :class="{ 'is-visible': visibleIds.includes('txt-big-r') }">Примеры применения</p>
    

    
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
import gallery2 from '@/assets/carousel/photo/1.png';
import gallery1 from '@/assets/carousel/photo/2.webp';
import gallery3 from '@/assets/carousel/photo/3.webp';

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
          title: 'Выставочный зал',
          description: 'Уникальные образцы работ'
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
      'section1',
      'section2',
      'section3',
      'section4',
      'section5',
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
      'card5-3',
      'contact-info'
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
  min-height: 100vh;
  padding: 2rem;
  background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0)), url('@/assets/m_img.png');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 2rem;
  position: relative;
}

.fr1-1 {
  max-width: 800px;
  text-align: center;
  opacity: 0;
  transform: translateY(-40px);
  transition: all 0.8s ease-out;
  background: rgba(0, 0, 0, 0.4);
  padding: 2.5rem;
  border-radius: 20px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}

.fr1-1:hover {
  border-color: rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(255, 255, 255, 0.1);
  transform: translateY(-5px);
}

.txt1 {
  font-size: clamp(2.5rem, 5vw, 4rem);
  margin-bottom: 1.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #ffffff 0%, #dedede 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 0 30px rgba(255, 255, 255, 0.1);
  letter-spacing: -0.02em;
}

.sec_txt {
  font-size: clamp(1.2rem, 2vw, 1.8rem);
  opacity: 0.9;
  font-weight: 400;
  margin: 0.5rem 0;
  color: #ffffff;
}

/* Элементы преимуществ */
.fr-elements {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  width: 100%;
  max-width: 1200px;
  margin: 3rem auto 0;
  padding: 0 2rem;
}

.fr-element {
  background: rgba(255, 255, 255, 0.05);
  padding: 2rem;
  border-radius: 15px;
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.5s ease;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(5px);
}

.fr-element:hover {
  transform: translateY(-5px);
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(255, 255, 255, 0.05);
}

.txt-element {
  font-size: 1.5rem;
  font-weight: 500;
  text-align: center;
  color: #FFFFFF;
  line-height: 1.4;
}

/* Текстовый блок */
.fr-2 {
  width: 100%;
  padding: 6rem 2rem;
  background: linear-gradient(to bottom, rgba(28, 26, 28, 1), rgba(28, 26, 28, 0.95));
  position: relative;
}

.fr-2::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
}

.text-sections {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2.5rem;
  max-width: 1200px;
  margin: 0 auto;
}

.text-section {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 20px;
  padding: 2.5rem;
  border: 1px solid rgba(255, 255, 255, 0.05);
  transition: all 0.3s ease;
}

.text-section:hover {
  background: rgba(255, 255, 255, 0.05);
  transform: translateY(-5px);
  border-color: rgba(255, 255, 255, 0.1);
}

.section-title {
  font-size: 1.8rem;
  margin-bottom: 1.5rem;
  color: #FFFFFF;
  font-weight: 600;
  position: relative;
  padding-bottom: 1rem;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 60px;
  height: 2px;
  background: linear-gradient(90deg, #ffffff, transparent);
}

.section-text {
  font-size: 1.1rem;
  line-height: 1.7;
  color: rgba(255, 255, 255, 0.8);
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
  margin: 4rem auto;
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
}

.carousel-wrapper {
  display: flex;
  transition: transform 0.7s ease;
  height: 600px;
  width: 100%;
}

.carousel-slide {
  flex: 0 0 100%;
  position: relative;
  overflow: hidden;
  width: 100%;
}

.carousel-slide img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.7s ease;
  display: block;
}

.carousel-slide:hover img {
  transform: scale(1.05);
}

.slide-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.8));
  padding: 3rem 2rem;
  transform: translateY(0);
  transition: transform 0.5s ease;
}

.slide-overlay h3 {
  font-size: 2.2rem;
  margin: 0 0 1rem;
  font-weight: 700;
  background: linear-gradient(135deg, #ffffff, #dedede);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.slide-overlay p {
  font-size: 1.2rem;
  opacity: 0.9;
  max-width: 600px;
}

.carousel-button {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(255, 255, 255, 0.15);
  border: none;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  cursor: pointer;
  color: white;
  font-size: 1.8rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  backdrop-filter: blur(5px);
}

.carousel-button:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: translateY(-50%) scale(1.1);
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
  padding: 4rem 2rem;
  text-align: center;
  background: linear-gradient(rgba(28, 26, 28, 0.8), rgba(28, 26, 28, 0.95));
}

.txt-big-m {
  font-size: 2.5rem;
  margin-bottom: 2rem;
  font-weight: 600;
  background: linear-gradient(45deg, #fff, #dedede);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.fr-5-1 {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 3rem auto;
}

.card5 {
  background: rgba(255, 255, 255, 0.05);
  padding: 2.5rem;
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
  backdrop-filter: blur(5px);
}

.card5:hover {
  transform: translateY(-10px);
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.2);
}

.card5txtb {
  font-size: 2rem;
  margin-bottom: 1rem;
  font-weight: 600;
  background: linear-gradient(45deg, #fff, #dedede);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.card5txts {
  font-size: 1.2rem;
  opacity: 0.8;
  line-height: 1.6;
}

/* Границы разделов */
.fr-2, .fr-3, .fr-4, .fr-5 {
  border-top: 1px solid rgba(189, 189, 189, 0.32);
}

/* Адаптивность */
@media (max-width: 768px) {
  .fr_1 {
    min-height: 100vh;
    padding: 2rem 1rem;
  }

  .fr1-1 {
    padding: 2rem;
  }

  .fr-elements {
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
  }

  .text-sections {
    gap: 2rem;
  }

  .section-title {
    font-size: 1.6rem;
  }
}

@media (max-width: 480px) {
  .fr1-1 {
    padding: 1.5rem;
  }

  .fr-elements {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .text-section {
    padding: 1.5rem;
  }

  .section-title {
    font-size: 1.4rem;
  }
}

.gallery-carousel {
  margin: 2rem auto;
  background: rgba(255, 255, 255, 0.05);
}

.gallery-carousel .carousel-slide img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  background: rgba(0, 0, 0, 0.3);
  display: block;
}

.gallery-carousel .carousel-wrapper {
  width: 100%;
  height: 600px;
}

.gallery-carousel .carousel-slide {
  width: 100%;
  height: 100%;
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

.contact-info {
  position: absolute;
  top: 2rem;
  left: 2rem;
  background: rgba(0, 0, 0, 0.6);
  padding: 1rem 1.5rem;
  border-radius: 10px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  z-index: 10;
  opacity: 0;
  transform: translateX(-20px);
  transition: all 0.5s ease;
}

.contact-info.is-visible {
  opacity: 1;
  transform: translateX(0);
}

.contact-text {
  margin: 0.3rem 0;
  font-size: 1rem;
  color: #ffffff;
}

.contact-link {
  color: #ffffff;
  text-decoration: none;
  transition: all 0.3s ease;
  display: inline-block;
}

.contact-link:hover {
  color: #dedede;
  transform: translateX(5px);
}

@media (max-width: 768px) {
  .contact-info {
    position: relative;
    top: 0;
    left: 0;
    margin: 1rem auto;
    width: fit-content;
  }
}
</style>