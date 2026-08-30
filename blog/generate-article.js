const fs = require('fs');
const path = require('path');

// خواندن قالب مادر
const templatePath = path.join(__dirname, 'template.html');
const template = fs.readFileSync(templatePath, 'utf8');

// خواندن داده‌های مقاله
const dataPath = path.join(__dirname, 'article-data.json');
const data = JSON.parse(fs.readFileSync(dataPath, 'utf8'));

// تولید FAQ Schema
const faqSchema = data.faq && data.faq.length > 0 ? `
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": ${JSON.stringify(data.faq.map(item => ({
    "@type": "Question",
    "name": item.question,
    "acceptedAnswer": {
      "@type": "Answer",
      "text": item.answer
    }
  })), null, 2)}
}
</script>
` : '';

// تولید بخش FAQ در HTML
const faqSection = data.faq && data.faq.length > 0 ? `
<section class="faq-section">
    <h2>❓ سوالات متداول</h2>
    ${data.faq.map(item => `
    <div class="faq-item">
        <div class="faq-question">${item.question}</div>
        <div class="faq-answer">${item.answer}</div>
    </div>
    `).join('')}
</section>
` : '';

// جایگزینی متغیرها در قالب
let finalHTML = template
    .replace(/\{\{TITLE\}\}/g, data.title)
    .replace(/\{\{SUBTITLE\}\}/g, data.subtitle)
    .replace(/\{\{DESCRIPTION\}\}/g, data.description)
    .replace(/\{\{KEYWORDS\}\}/g, data.keywords)
    .replace(/\{\{PUBLISH_DATE\}\}/g, data.publish_date)
    .replace(/\{\{MODIFIED_DATE\}\}/g, data.modified_date)
    .replace(/\{\{OG_IMAGE\}\}/g, data.og_image)
    .replace(/\{\{CANONICAL_URL\}\}/g, data.canonical_url)
    .replace(/\{\{OG_TITLE\}\}/g, data.title)
    .replace(/\{\{OG_DESCRIPTION\}\}/g, data.description)
    .replace(/\{\{OG_URL\}\}/g, data.canonical_url)
    .replace(/\{\{TWITTER_TITLE\}\}/g, data.title)
    .replace(/\{\{TWITTER_DESCRIPTION\}\}/g, data.description)
    .replace(/\{\{TWITTER_IMAGE\}\}/g, data.og_image)
    .replace(/\{\{BREADCRUMB_TITLE\}\}/g, data.title.split(':')[0])
    .replace(/\{\{FAQ_SCHEMA\}\}/g, faqSchema)
    .replace(/\{\{FAQ_SECTION\}\}/g, faqSection)
    .replace(/\{\{CONTENT\}\}/g, data.content);

// ذخیره فایل نهایی
const outputDir = path.join(__dirname, 'blog');
if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir);
}

const slug = data.canonical_url.split('/').filter(Boolean).pop();
const outputPath = path.join(outputDir, `${slug}.html`);
fs.writeFileSync(outputPath, finalHTML, 'utf8');

console.log(`✅ مقاله با موفقیت تولید شد: ${outputPath}`);
console.log(`📊 تعداد سوالات متداول: ${data.faq ? data.faq.length : 0}`);