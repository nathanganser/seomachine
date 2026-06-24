---
title: "Component Template"
description: "All components in one page"
---

<!--
=================================================================
IMAGE & MEDIA COMPONENTS
=================================================================
-->

<!--
Base image component
Can be used as a child to load images
Props:
  - src (string, required) — relative path to /images/visuals/
  - alt (string, default: "Magic Heidi illustration")
  - quality (number) — image quality setting
  - format (string) — image format override
Locale pattern: use {locale} placeholder for translated images
Also supports one-liner syntax: :image-view{src="..." alt="..."}
-->
::image-view
---
src: "invoice-list.{locale}.webp"
alt: "Magic Heidi Invoice List"
---
::

<!-- Media component. Useful for showing youtube video.
     Inherits ALL hero-basic props: label, title, subtitle, theme, orientation, fullscreen, reverse, etc.
     reverse defaults to true (video on left). -->
::hero-media
---
label: Video Demo
title: "Watch How It <span>Works</span>"
subtitle: "A quick overview."
orientation: horizontal
youtube:
  id: "vLMAjtVM-Gg"
---
::

<!-- Video component. Useful for showing looping video files without audio. Files are hosted in /images/visuals/ -->
::hero-media
---
video:
  src: "demo.mp4"
---
::

<!--
=================================================================
HERO-BASIC
The foundational layout component. Most section components extend it.
=================================================================
Props:
  - label (string, optional) — small uppercase label above title
  - title (string, required) — main heading (supports HTML: <span>, <br>). 4-5 words ideally.
  - subtitle (string, optional) — text below title. Target 1 sentence, ≤20 words. Hard cap 2 sentences. Inline HTML supported (<span>, <br>, <strong>, <em>, <a href="…">…</a>). For feature sections, append `<a href="/feature-path">Mehr zu X →</a>` at the end of the subtitle to deep-link to the matching feature page (/invoicing, /ai-expenses-scanning, /accounting, /vat-management, /bank-statement-import, /security, /customer-management, /quotes, /web, /iphone, /mac, /windows, /freelancer). Long multi-clause subtitles read as filler — trim ruthlessly.
  - theme ('light' | 'dark', default 'light') — color scheme
  - orientation ('vertical' | 'horizontal', default 'vertical') — layout direction
  - fullscreen (boolean) — centers content in 100vh
  - reverse (boolean) — flips content/child order in horizontal layout
  - innerClass (string) — custom class on content grid
  - headerClass (string) — custom class on header column
  - titleClass (string) — custom class on title element
  - subtitleClass (string) — custom class on subtitle element
  - disableAnimations (boolean) — turns off intersection-observer animations

Named slots: label, title, subtitle, header-body, before-content, default

Background classes (applied via {.class-name} syntax):
  .bg-hero-gradient-1  — primary gradient
  .bg-hero-gradient-2  — secondary gradient
  .bg-white            — white
  .bg-cream            — cream
  .bg-coral            — coral (use with theme: dark)
  .bg-dark-nav         — dark navigation color
  .pain-gradient       — pain section gradient
  .bg-gradient-to-b.from-red-50.to-white — custom Tailwind gradient
-->

::hero-basic{.bg-hero-gradient-1}
---
label: Hero Label
fullscreen: true
orientation: horizontal
title: Hero Basic with <span>Background</span><br> and Visual
subtitle: Hero basic subtitle text.
---
:visuals-invoice-list-page
::

::hero-basic
---
label: Another Section
title: Hero Basic Default Background
subtitle: Default hero basic subtitle.
---

  ::detailed-feature-list
  ---
  items:
    - label: Category One
      title: Detailed feature headline
      subtitle: Detailed feature subtitle.
      features:
        - Bullet point one
        - Bullet point two
        - Bullet point three
      image:
        src: "invoice-list.{locale}.webp"
        alt: "Magic Heidi Banner"
  ---
  ::
::

<!-- hero-basic with reverse layout (content right, child left) -->
::hero-basic{.bg-white}
---
orientation: horizontal
reverse: true
label: Reversed
title: "Reversed <span>Layout</span>"
subtitle: "Content on the right, child component on the left."
---
:visuals-invoice-list-page
::

::hero-basic{.bg-coral}
---
theme: dark
label: Dark Section
title: "Hero Basic Coral Background"
subtitle: Dark theme section subtitle.
---
  ::feature-grid
  ---
  id: dark-feature-grid
  items:
    - title: Two Column Feature One
      description: Two column grid description.
    - title: Two Column Feature Two
      description: Another two column description.
    - title: Two Column Feature Three
      description: Third description.
  ---
  ::

  ::hero-cta-links
  ---
  title: CTA Section Title
  subtitle: CTA section subtitle.
  links:
    - label: Primary Button
      url: /start
      variant: primary
    - label: Secondary Button
      url: https://example.com
  style:
    margin-top: 120px
  ---
  ::
::

<!--
=================================================================
FEATURE-IMAGE
Extends hero-basic. Shows a hero section with an image.
=================================================================
Props (in addition to all hero-basic props):
  - image (required) — { src: string, alt?: string }
  - alt (boolean) — switches to card-style layout (white bg, shadow, 2-col grid)
  - title (string, optional — unlike hero-basic where required)
-->

<!-- Standard horizontal feature-image. Ideal for blog/article hero or product feature sections. -->
::feature-image
---
label: AI-Powered
orientation: horizontal
title: "Expense Tracking That <span>Does Itself</span>"
subtitle: "Paper receipts are the enemy of freelancers. Lost. Faded. Forgotten. Snap a photo — Magic Heidi's AI extracts the date, amount, VAT, category, and vendor automatically. No more manual data entry. No more shoeboxes of receipts."
image:
  src: "expenses-mobile.{locale}.webp"
  alt: "Magic Heidi Expensing on Mobile"
---
::

<!-- Contains an invoice animation on the right side of the page, and sign up CTAs -->
::pages-landing-hero-section
---
stats:
  - label: Stat Label
    value: 5,000+
  - label: Another Stat
    value: 4.9★
  - label: Third Stat
    value: 30 sec
subtitle: Short subtitle text with <em>emphasis</em> if needed.
title: Main Headline with <span>Highlight</span>
---
::

<!-- Fullscreen feature-image -->
::feature-image
---
fullscreen: true

image:
  src: "analytics.{locale}.webp"
  alt: "Magic Heidi Analytics Dashboard"
---
::

<!-- feature-image with alt layout (card style: white bg, shadow, 2-col grid) -->
::feature-image
---
alt: true
title: "Card Style <span>Layout</span>"
subtitle: "With alt=true, renders as a 2-column card with white bg and shadow."
image:
  src: "invoice-list.{locale}.webp"
  alt: "Magic Heidi Invoice List"
---
::

<!-- feature-image with reverse (image on left) -->
::feature-image
---
orientation: horizontal
reverse: true
title: "Reversed <span>Image Position</span>"
subtitle: "Image appears on the left, text on the right."
image:
  src: "analytics.{locale}.webp"
  alt: "Magic Heidi Analytics"
---
::

<!--
=================================================================
FEATURE-SHOWCASE
Horizontal hero section with image + highlights (emoji/title/description).
Extends hero-basic. Great for product reviews, detailed feature sections.
=================================================================
Props (in addition to all hero-basic props):
  - image (required if no video) — { src: string, alt?: string }
  - video (alternative to image) — { src: string } — looping silent .mp4. Prefer video over image when an animation file exists for the topic (e.g. invoice-gen.{locale}.mp4 for the invoicing showcase).
  - highlights (HighlightItem[], optional):
      - icon (string) — emoji displayed to the left
      - title (string) — short heading
      - description (string) — supporting text (supports inline markdown)
Defaults: orientation=horizontal
-->

<!-- Feature showcase with image right, highlights left -->
::feature-showcase
---
label: Product Showcase
title: "Everything You Need to <span>Invoice Professionally</span>"
subtitle: "Built for Swiss freelancers who want to spend less time on admin."
image:
  src: "invoice-list.{locale}.webp"
  alt: "Magic Heidi Invoice List"
highlights:
  - icon: "🇨🇭"
    title: Swiss QR Invoices
    description: "Generate compliant QR invoices accepted by all Swiss banks in seconds."
  - icon: "🤖"
    title: AI-Powered Expenses
    description: "Snap a receipt — our AI extracts amount, VAT, category, and vendor automatically."
  - icon: "📊"
    title: Tax-Ready Reports
    description: "Export clean reports your accountant will love. Always audit-ready."
---
::

<!-- Feature showcase with VIDEO (looping .mp4) instead of image — confirmed working -->
::feature-showcase
---
label: Magic Heidi
title: "Buchhaltung, Faktura und Spesen <span>in einer App</span>"
subtitle: "Eine App für die drei Werkzeuge, die du täglich brauchst."
video:
  src: "invoice-gen.{locale}.mp4"
highlights:
  - icon: "🇨🇭"
    title: Swiss QR Invoices
    description: "SIX-konforme QR-Rechnungen, deine Kunden zahlen mit einem Scan."
  - icon: "🤖"
    title: KI-Belegscan
    description: "Foto vom Beleg, Magic Heidi liest Datum, Betrag und MWST heraus."
  - icon: "📊"
    title: MWST automatisch
    description: "Magic Heidi rechnet jede Rechnung korrekt, du übernimmst die Quartalszahlen."
---
::

<!-- Feature showcase reversed (image on left) with dark theme -->
::feature-showcase
---
theme: dark
reverse: true
title: "Why Freelancers <span>Love Us</span>"
subtitle: "Join thousands of Swiss freelancers who switched to Magic Heidi."
image:
  src: "analytics.{locale}.webp"
  alt: "Magic Heidi Analytics"
highlights:
  - icon: "⚡"
    title: 30-Second Invoices
    description: "Create and send a professional invoice in under 30 seconds."
  - icon: "🔒"
    title: Bank-Grade Security
    description: "Your data is encrypted and hosted on Swiss servers."
  - icon: "💬"
    title: Stellar Support
    description: "Real humans who respond within hours, not days."
---
::

<!--
=================================================================
FEATURE-GRID
Flexible grid of feature cards. Nest inside hero-basic.
=================================================================
Props:
  - items (FeatureItem[], required):
      - title (string)
      - description (string)
      - icon (string, optional) — emoji or icon
      - link (string, optional) — makes item a clickable NuxtLink
      - features (string[], optional) — bullet list under description
  - itemWidth (string, default '300px') — e.g. '200px' for 4 cols, '300px' for 3 cols
  - headingLevel ('h2' | 'h3' | 'h4', default 'h3') — heading semantics
  - theme ('base' | 'elevated' | 'dark', default 'base'):
      base     — bordered cards on transparent bg
      elevated — white bg cards (great on cream/colored sections)
      dark     — translucent dark cards (pair with theme: dark hero-basic)
  - schemaType ('ItemList' | 'Service' | 'Product', default 'ItemList') — schema.org structured data
-->

<!-- feature-grid with bullet list features per item -->
::hero-basic{.bg-white}
---
label: Grid with Lists
title: "Feature Grid with <span>Bullet Lists</span>"
subtitle: "Each item can have a features array."
---

  ::feature-grid
  ---
  id: grid-with-features
  item-width: 300px
  items:
    - title: Invoicing
      description: Create and manage invoices.
      icon: 🧾
      features:
        - QR code generation
        - PDF export
        - Multi-currency
    - title: Expenses
      description: Track all your expenses.
      icon: 📸
      features:
        - AI receipt scanning
        - Category auto-detect
        - Bank import
    - title: Accounting
      description: Stay tax-ready all year.
      icon: 📊
      features:
        - VAT reports
        - Profit & loss
        - Year-end export
  ---
  ::
::

<!-- feature-grid with elevated theme on cream bg (4 cols via item-width: 200px) -->
::hero-basic{.bg-cream}
---
label: Elevated
title: "Elevated Theme <span>Grid</span>"
subtitle: "White card backgrounds on cream section."
---

  ::feature-grid
  ---
  id: elevated-grid
  theme: elevated
  item-width: 200px
  items:
    - title: Card One
      description: White background card.
      icon: ✨
    - title: Card Two
      description: Elevated card style.
      icon: 🎯
    - title: Card Three
      description: Great on cream backgrounds.
      icon: 🚀
    - title: Card Four
      description: Fourth card example.
      icon: 💳
  ---
  ::
::

<!-- feature-grid with clickable items -->
::hero-basic{.bg-white}
---
label: Linked Items
title: "Clickable Grid <span>Items</span>"
subtitle: "Items with link prop become navigable."
---

  ::feature-grid
  ---
  id: linked-grid
  item-width: 250px
  items:
    - title: Invoicing
      description: Learn about invoicing.
      icon: 🧾
      link: /invoicing
    - title: Pricing
      description: See pricing plans.
      icon: 💰
      link: /pricing
    - title: Features
      description: Explore all features.
      icon: ✨
      link: /features
  ---
  ::
::

<!--
=================================================================
DETAILED-FEATURE-LIST
Two-column cards with image + feature bullets. Nest inside hero-basic.
See "Hero Basic Default Background" example above.
=================================================================
Props:
  - items (DetailedFeatureItem[], required):
      - label (string) — uppercase category label
      - title (string) — heading (supports HTML: <span>)
      - subtitle (string) — description paragraph
      - features (string[]) — bullet list
      - image ({ src: string, alt: string }) — side image
-->

<!--
=================================================================
MARKDOWN
Styled markdown content wrapper.
=================================================================
Props:
  - boxed (boolean) — wraps in rounded box (white bg + shadow, or translucent glass in dark). Not to be used too much.
  - theme ('light' | 'dark') — dark = full-width navy bg
  - pt (string) — custom padding-top CSS value (default: 32px)
  - pb (string) — custom padding-bottom CSS value (default: 32px)
  - noContainer (boolean) — renders without Container wrapper (no max-width, no padding)
  - as (HTML tag) — changes wrapper element (default: 'section', use 'article' for blog content)
-->

<!-- Renders styled markdown content -->
::markdown
---
boxed: true
---

# A short history of Magic Heidi
Magic Heidi is a Swiss software company.

> Founded in 2022
::

<!-- Markdown with dark theme -->
::markdown
---
boxed: true
theme: dark
pt: 0px
pb: 40px
---
**Bold intro text.** Body content here — the box uses a translucent dark style matching adjacent dark sections.
::

<!-- Markdown with noContainer (no wrapper). Use `as: article` for blog content semantics. -->
::markdown
---
noContainer: true
---
Raw markdown without any Container wrapper. Useful inside other components.
::

<!--
=================================================================
LANDING PAGE COMPONENTS
=================================================================
-->

::pages-landing-pain
---
items:
  - icon: ⚡
    title: Short benefit
    subtitle: Brief subtitle
  - icon: 📸
    title: Another benefit
    subtitle: Another subtitle
  - icon: 📊
    title: Third benefit
    subtitle: Third subtitle
subtitle: "Longer paragraph explaining the pain point or problem your audience faces."
title: "Problem <span>Statement</span>.<br>Second Line Here."
---
::

::pages-landing-invoice-showcase
---
features:
  - icon: 🧾
    title: Feature One
    subtitle: Feature description
  - icon: ⚡
    title: Feature Two
    subtitle: Another description
  - icon: ✨
    title: Feature Three
    subtitle: Third description
  - icon: 🌍
    title: Feature Four
    subtitle: Fourth description
badge: Section Badge
subtitle: "Section subtitle explaining this feature showcase."
title: "Showcase Headline in <span>30 Seconds</span>"
---
::

::pages-landing-features
---
label: Features
title: |
  Features Section Title<br/>
  Second Line Here.
subtitle: Features section subtitle text.
items:
  - icon: 📄
    title: Feature Category One
    description: Feature description with <strong>bold text</strong> if needed.
    features:
      - Bullet point one
      - Bullet point two
      - Bullet point three
      - Bullet point four
  - icon: 🤖
    title: Feature Category Two
    description: Another feature description paragraph.
    features:
      - Another bullet
      - More details
      - Third point
      - Fourth point
  - icon: 📊
    title: Feature Category Three
    description: Third feature description here.
    features:
      - Feature detail
      - Another detail
      - Third detail
      - Fourth detail
---
::

::pages-landing-swiss-section
---
title: |
  Two Line Title.<br/>
  <span>With Highlight.</span>
description: "Description paragraph explaining Swiss-specific features or local focus."
features:
  - icon: 📋
    title: Local Feature
    subtitle: Feature subtitle. 1 sentence max.
  - icon: 💰
    title: Another Feature
    subtitle: Another subtitle. 1 sentence max.
  - icon: 🏦
    title: Third Feature
    subtitle: Third subtitle. 1 sentence max.
  - icon: 🌐
    title: Fourth Feature
    subtitle: Fourth subtitle. 1 sentence max.
badges:
  - icon: 🇨🇭
    label: Badge One
  - icon: 🔒
    label: Badge Two
  - icon: 💬
    label: Badge Three
  - icon: ⭐
    label: Badge Four
---
::

::pages-landing-comparison
---
label: Comparison
title: "Product vs. Alternatives"
subtitle: "Comparison section subtitle."
table:
  columns:
    - label: Feature
    - label: Our Product
      highlight: true
    - label: Competitor A
    - label: Competitor B
    - label: Competitor C
  rows:
    - label: Price
      values:
        - text: CHF 30
          highlight: true
        - text: CHF 45+
        - text: CHF 35+
        - text: CHF 40+
    - label: Target User
      values:
        - text: <span class="check">✓</span> Freelancers
          highlight: true
        - text: <span class="cross">✗</span> SMEs
        - text: <span class="cross">✗</span> SMEs
        - text: <span class="cross">✗</span> SMEs
    - label: Setup Time
      values:
        - text: 2 minutes
          highlight: true
        - text: 30+ minutes
        - text: 15+ minutes
        - text: 20+ minutes
    - label: AI Features
      values:
        - text: <span class="check">✓</span> Included
          highlight: true
        - text: <span class="cross">✗</span> No
        - text: <span class="partial">⚠</span> Limited
        - text: <span class="partial">⚠</span> Limited
---
::

<!--
hero-reviews
Props:
  - label, title, subtitle (standard)
  - cta (optional) — { label: string, url: string }
  - items[]:
      - quote (string)
      - author (string)
      - role (string)
      - link (string, optional) — URL to the source review page (Capterra, Google, Trustpilot, App Store, etc.). Renders the review card as a clickable link to the source.
      - avatarUrl (string, optional) — custom avatar image (falls back to DiceBear generated)

Convention: when reviews come from public review sites, set `link:` on each item so visitors can click through to verify. Use the source's name in `author` (e.g., "Capterra Bewertung", "Google Bewertung", "Trustpilot Bewertung") and put the rating + a "alle Bewertungen lesen" hint in `role`.
-->
::hero-reviews
---
label: Testimonials
title: "What Users Say"
subtitle: "Testimonials section subtitle."
cta:
  label: Join them today
  url: /start
items:
  - quote: "First testimonial — short, specific, mentions an outcome or workflow win."
    author: "Capterra Bewertung"
    role: "4.7★ — alle Bewertungen lesen"
    link: "https://www.capterra.com/p/10020344/Magic-Heidi/"
  - quote: "Second testimonial referencing a different angle or product strength."
    author: "Google Bewertung"
    role: "5.0★ — alle Bewertungen lesen"
    link: "https://maps.app.goo.gl/KD7uvvF2vJGNupxR8"
  - quote: "Third testimonial. Different source, different angle keeps it credible."
    author: "Trustpilot Bewertung"
    role: "4.5★ — alle Bewertungen lesen"
    link: "https://www.trustpilot.com/review/magicheidi.ch"
---
::

<!--
pages-landing-video-reviews — Tella.tv video testimonial grid
Props:
  - label, title, subtitle (standard)
  - items[]:
      - title (string)
      - subtitle (string)
      - embedId (string) — Tella.tv embed ID
      - url (string) — direct link to video
-->
::pages-landing-video-reviews
---
label: Video Testimonials
title: "See What Users <span>Have to Say</span>"
subtitle: "Real video testimonials from Magic Heidi users."
items:
  - title: "How I invoice in 30 seconds"
    subtitle: "A freelancer shows the full workflow."
    embedId: "example-embed-id"
    url: "https://www.tella.tv/video/example"
  - title: "Expense tracking made easy"
    subtitle: "AI scans receipts automatically."
    embedId: "example-embed-id-2"
    url: "https://www.tella.tv/video/example2"
---
::

::pages-landing-plans
---
title: Simple Pricing. No Surprises.
subtitle: One plan. All features. Cancel anytime.
plans:
  - title: Free Trial
    price:
      amount: 0
      details: Forever
    cta:
      label: Start Free
      url: "/start"
    features:
      - 3 invoices
      - 3 expenses
      - All features unlocked
      - No credit card required

  - title: Annual
    badge: Most Popular
    price:
      amount: 24.99
      details: Billed Annually at CHF 299

    cta:
      label: Start Annual — Save 17%
      url: "/start"
    featured: true
    features:
      - Unlimited invoices
      - Unlimited expenses
      - AI expense scanning
      - All platforms included
      - Bank statement import
      - Swiss VAT management
      - Priority support
  - title: Monthly
    price:
      amount: 30
      details: Flexible, cancel anytime
    cta:
      label: Start Monthly
      url: "/start"
    features:
      - Unlimited invoices
      - Unlimited expenses
      - AI expense scanning
      - All platforms included
      - Bank statement import
      - Swiss VAT management
guarantee: 30-day money-back guarantee. Try it risk-free.
---
::

::pages-landing-faq
---
label: FAQ
title: "Frequently Asked Questions"
items:
  - question: First question here?
    answer: First answer with detailed explanation.
  - question: Second question here?
    answer: Second answer with helpful information.
  - question: Third question here?
    answer: Third answer explaining features or policies.
---
::

::pages-landing-final-cta
---
title: "Final CTA Headline"
subtitle: "Final CTA subtitle encouraging action."

# Redirects to app
primary: "Sign Up"

# Second CTA
secondary:
  label: "Learn more"
  url: /help
---
::

<!--
=================================================================
HERO-CTA-LINKS
CTA card with title/subtitle + button links.
ALWAYS nest inside hero-basic for proper section padding and background.
Do not use as a top-level component on its own.
=================================================================
Props:
  - title (string) — card headline
  - subtitle (string) — supporting text below the title
  - links (CTAButtonProps[]):
      - label (string)
      - url (string, required) — internal path (/start), external URL, or asset URL
      - variant ('primary' | 'secondary')
      - icon (string, optional) — emoji rendered inside the button (e.g. 📝, 📕, ⬇️, ✨)
      - external (boolean, optional) — opens in new tab
  - style (object, optional) — inline CSS e.g. { margin-top: '120px' }

Pattern: keep title/subtitle on hero-cta-links, NOT on the hero-basic wrapper.
Use hero-basic only for section styling (background class, label, layout).
This avoids duplicate headlines and keeps the CTA card self-contained.
-->

<!-- Standalone CTA section (download buttons, sign-up, etc.) -->
::hero-basic{.bg-cream}
---
label: Download
---
  ::hero-cta-links
  ---
  title: "Hol dir die Vorlage jetzt"
  subtitle: "Word und PDF mit allen Pflichtangaben. Kostenlos, ohne Anmeldung."
  links:
    - label: Word herunterladen
      url: "https://example.com/template.docx"
      variant: primary
      icon: 📝
    - label: PDF herunterladen
      url: "https://example.com/template.pdf"
      variant: secondary
      icon: 📕
  ---
  ::
::


<!--
=================================================================
SOFTWARE SCHEMA (invisible — SEO only)
Adds schema.org SoftwareApplication structured data.
=================================================================
Props:
  - page-path (string) — page URL path
  - description (string) — app description
  - price (number) — price in CHF
  - feature-list (string[], optional) — list of features
-->
::pages-landing-magic-heidi-software-schema
---
page-path: /
description: "Swiss invoicing and accounting app for freelancers"
price: 30
feature-list:
  - QR invoicing
  - AI expense scanning
  - Swiss VAT management
---
::

<!--
=================================================================
BLOG COMPONENTS
=================================================================
-->

<!--
Blog header — renders the article title, description, publication date, and author display with structured data for SEO.

`::blog` may wrap `::markdown` blocks (with `as: article`) for the article body. It MUST NOT wrap other components — `::pages-landing-faq`, `::pages-landing-comparison`, `::feature-grid`, `::feature-image`, `::feature-showcase`, `::hero-reviews`, etc. all go AFTER `::blog`'s closing `::`, as siblings.

Place `::blog` first on the page (after page frontmatter). Indent nested `::markdown` blocks with 2 spaces.

Props:
  - date (string) — publication date - Write directly the date
  - title (string) — article title
  - description (string) — article description
  - author (AuthorData):
      - name (string)
      - description (string)
      - avatar (string) — avatar URL
-->
::blog
---
date: "15 June 2025"
title: "Example Blog Post"
description: "A description for SEO and preview."
author:
  name: "Nathan Ganser"
  description: "Founder of Magic Heidi"
  avatar: "https://magicheidi.ch/images/visuals/nathan.webp"
---

  ::markdown
  ---
  as: article
  ---
  Article body prose goes here. Add more `::markdown as: article` blocks for additional prose sections.
  ::

::

<!-- Structured components (FAQ, comparison, feature-grid, etc.) come AFTER `::blog`, as siblings -->
::pages-landing-faq
---
items:
  - question: "Example question?"
    answer: "Example answer."
---
::

<!-- Blog author data — standalone author profile display -->
::blog-author-data
---
author:
  name: "Nathan Ganser"
  description: "Founder of Magic Heidi"
  avatar: "https://magicheidi.ch/images/visuals/nathan.webp"
---
::

<!--
=================================================================
TUTORIALS INDEX
Auto-generates a listing of all tutorial pages grouped by category.
No props needed — queries content collection automatically.
=================================================================
-->
::tutorials-index
::

<!--
=================================================================
HELP / SUPPORT CARD
Contact card with email + phone CTAs.
=================================================================
Props:
  - title (string, optional — defaults to i18n "still_have_questions?")
  - subtitle (string, optional — defaults to i18n "all_lang_swiss_team_support")
-->
::help-info-card
---
title: "Need Help?"
subtitle: "Our Swiss team speaks your language."
---
::

<!--
=================================================================
INTERACTIVE TOOL COMPONENTS
All self-contained with no props required.
Drop into any content page.
=================================================================
-->

<!-- VAT add/remove calculator -->
::vat-calculator
::

<!-- Swiss salary calculator -->
::salary-calculator
::

<!-- Swiss monthly-to-hourly wage calculator (Stundenlohn-Rechner) -->
::hourly-wage-calculator
::

<!-- Swiss freelancer tax calculator -->
::freelancer-calculator
::

<!-- EUR/CHF converter with 12-month history -->
::currency-converter
::

<!-- Bitcoin price calculator with charts -->
::btc-price
::

<!-- Gold price calculator in multiple currencies -->
::gold-price
::

<!-- AI-powered business name generator -->
::business-name-generator
::

<!-- Full QR invoice PDF generator with form -->
::qr-invoice-generator
::

<!-- Embedded QR invoice iframe tool -->
::qr-invoice-tool
::

<!--
=================================================================
VISUAL COMPONENTS
Decorative illustrations. Can be added as children in hero-basic
or other components with slots.
=================================================================
-->

<!-- Shows a pdf visual of invoice.
     Props: referrerName (string), referrerLogoUrl (string) -->
:visuals-invoice-pdf

<!-- Shows a list of invoice items (full page view) -->
:visuals-invoice-list-page

<!-- Shows a compact list of invoices -->
:visuals-invoice-list