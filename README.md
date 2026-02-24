<h1 id="cryptpix-unbreakable-image-protection">CryptPix: Unbreakable Image Protection for Your Website</h1>

<p><strong>CryptPix</strong> is a cutting-edge, open-source solution designed to <strong>shield your website’s images from automated scraping and make manual extraction a daunting, near-impossible task</strong>. Crafted for seamless integration with Django, CryptPix employs a sophisticated, multi-tiered defense system that transforms your images into a fortress of security. Whether you’re safeguarding product photos on an e-commerce platform, protecting a photography portfolio, or securing proprietary visuals in any industry, CryptPix ensures your images remain yours—viewable only by legitimate users on your site. With its blend of robust protection, developer-friendly integration, and flawless user experience, CryptPix stands as the ultimate tool for defending your visual content against theft.</p>

<!-- Table of Contents -->
<div id="table-of-contents">
  <h2>Table of Contents</h2>
  <ul>
    <li><a href="#cryptpix-unbreakable-image-protection">CryptPix: Unbreakable Image Protection for Your Website</a>
      <ul>
        <li><a href="#what-cryptpix-does">What CryptPix Does</a></li>
        <li><a href="#how-it-works">How It Works: A High-Level View</a></li>
        <li><a href="#why-cryptpix-shines">Why CryptPix Shines</a></li>
        <li><a href="#seamless-integration-django">Seamless Integration with Django</a></li>
        <li><a href="#use-cases-benefits">Use Cases and Benefits</a></li>
        <li><a href="#why-choose-cryptpix">Why Choose CryptPix?</a></li>
      </ul>
    </li>
    <li><a href="#cryptpix-installation-integration">CryptPix Installation and Integration Instructions</a>
      <ul>
        <li><a href="#installation">Installation</a>
          <ul>
            <li><a href="#requirements">Requirements</a></li>
            <li><a href="#system-dependencies">System Dependencies</a></li>
          </ul>
        </li>
        <li><a href="#setup-django-project">Setup in Django Project</a>
          <ul>
            <li><a href="#add-installed-apps">Add to INSTALLED_APPS</a></li>
            <li><a href="#configure-urls">Configure URLs</a></li>
            <li><a href="#handle-static-files">Handle Static Files</a></li>
            <li><a href="#include-css-javascript">Include CSS and JavaScript</a></li>
            <li><a href="#run-migrations">Run Migrations</a></li>
          </ul>
        </li>
        <li><a href="#using-cryptpix-model-mixin">Using the CryptPix Model Mixin</a>
          <ul>
            <li><a href="#adding-mixin">Adding the Mixin</a></li>
            <li><a href="#configuring-source-field">Important: Configuring the Source Field</a></li>
            <li><a href="#example-model">Example Model</a></li>
            <li><a href="#what-happens">What Happens</a></li>
          </ul>
        </li>
        <li><a href="#security-modes-and-rendering-architecture">Security Modes and Rendering Architecture</a>
          <ul>
            <li><a href="#mode-1-secure-single-image-obfuscated-link">Mode 1: Secure Single Image (Obfuscated Link)</a></li>
            <li><a href="#mode-2-secure-single-image-with-visual-distortion">Mode 2: Secure Single Image with Visual Distortion</a></li>
            <li><a href="#mode-3-secure-split-layer-reconstruction">Mode 3: Secure Split-Layer Reconstruction</a></li>
            <li><a href="#stable-dom-contract">Stable DOM Contract</a></li>
            <li><a href="#css-integration-guidance">CSS Integration Guidance</a></li>
            <li><a href="#javascript-integration-guidance">JavaScript Integration Guidance</a></li>
          </ul>
        </li>
      </ul>
    </li>
    <li><a href="#integration-usage">Integration and Usage</a>
      <ul>
        <li><a href="#template-tags">Template Tags</a>
          <ul>
            <li><a href="#load-tags">Load the Tags</a></li>
            <li><a href="#render-protected-image">Render the Protected Image</a></li>
            <li><a href="#using-breakpoints">Using Breakpoints</a>
              <ul>
                <li><a href="#explanation-breakpoints">Explanation</a></li>
                <li><a href="#use-breakpoints-effectively">To use breakpoints effectively</a></li>
                <li><a href="#include-css">Include CSS</a></li>
              </ul>
            </li>
            <li><a href="#how-image-served">How the Image Is Served</a></li>
            <li><a href="#protecting-original-image">Protecting the Original Image</a></li>
          </ul>
        </li>
        <li><a href="#configuration-options">Configuration Options</a></li>
        <li><a href="#running-testing">Running and Testing</a>
          <ul>
            <li><a href="#running-server">Running the Server</a></li>
            <li><a href="#example-setup">Example Setup</a></li>
            <li><a href="#verifying-works">Verifying It Works</a></li>
          </ul>
        </li>
        <li><a href="#admin-previews">Admin Previews</a></li>
        <li><a href="#troubleshooting-tips">Troubleshooting Tips</a></li>
      </ul>
    </li>
  </ul>
</div>

<h3 id="what-cryptpix-does">What CryptPix Does</h3>

<p>CryptPix revolutionizes image protection by rendering your images <strong>unusable to scrapers</strong> while preserving their pristine quality for authorized viewers. Through a series of carefully engineered security layers, it transforms your images into a format that defies both automated bots and determined manual scrapers. Even if a scraper manages to download an image, what they get is a scrambled, incoherent mess—utterly useless without the specific conditions provided by your website’s rendering process. CryptPix achieves this without watermarks, overlays, or other obtrusive methods that degrade the user experience. Instead, it delivers crystal-clear visuals to your audience while ensuring that stolen assets are worthless.</p>

<h3 id="how-it-works">How It Works: A High-Level View</h3>

<p>At its heart, CryptPix integrates seamlessly with your Django application to protect images from the moment they’re uploaded. When you add an image to a model, CryptPix automatically processes it into a secure format, storing the necessary metadata to display it correctly. These images are served through tightly controlled, time-sensitive access mechanisms that restrict delivery to authorized users only. In the browser, CryptPix orchestrates a precise reconstruction process, ensuring images render correctly with pixel-perfect clarity. This tag provides essential styling to align and display the protected images, making it a critical component of the rendering process. The result is a system where images appear perfectly to legitimate visitors but remain indecipherable to anyone attempting to bypass your site’s protections.</p>

<p>The first layer of defense ensures that images are only accessible through secure, ephemeral channels tied to a user’s session, preventing bots from grabbing direct links or reusing URLs. The second layer transforms the image data into a format that’s meaningless outside the context of your website, rendering any downloaded file useless. The final layer leverages dynamic client-side rendering to reconstruct the image, requiring specific conditions that only your site can provide. Together, these layers create a system where scraping an image yields nothing but a garbled artifact, while legitimate users enjoy a flawless viewing experience.</p>

<h3 id="why-cryptpix-shines">Why CryptPix Shines</h3>

<p>Unlike traditional anti-scraping methods—such as watermarks that deface images, hotlink prevention that’s easily bypassed, or heavy server-side restrictions that slow performance—CryptPix offers a smarter, more resilient solution. Most alternatives rely on superficial barriers that savvy scrapers can circumvent with minimal effort. CryptPix, by contrast, fundamentally alters the image data itself, ensuring that even successful downloads are worthless without the intricate client-side logic only your site provides. This makes it exponentially harder for scrapers to succeed, as they face not just technical hurdles but a labyrinth of protections that require reverse-engineering multiple layers of security.</p>

<p>What sets CryptPix apart is its balance of <strong>security</strong>, <strong>simplicity</strong>, and <strong>scalability</strong>. It delivers ironclad protection without compromising performance or adding complexity to your workflow. The images remain pixel-perfect for users, with no visible artifacts or delays, while scrapers are left with unusable data. Its open-source nature invites community contributions, ensuring it evolves to counter new scraping techniques. Whether you’re protecting a single hero image or an entire gallery, CryptPix scales effortlessly, offering enterprise-grade security in a lightweight, developer-friendly package.</p>

<h3 id="seamless-integration-django">Seamless Integration with Django</h3>

<p>Getting started with CryptPix is straightforward, thanks to its tight integration with Django. Installation is a breeze:</p>

<ol>
  <li>Install via pip: <code>pip install cryptpix</code></li>
  <li>Add the <code>CryptPixModelMixin</code> to any Django model with an image field.</li>
  <li>Include the <code>{% cryptpix_css %}</code> template tag in your templates to provide the necessary styling for correct image rendering.</li>
  <li>Use the <code>{% cryptpix_image %}</code> template tag to embed protected images in your templates.</li>
</ol>

<p>Here’s an example of how to use CryptPix in your templates:</p>

<pre><code class="language-html">{% load cryptpix_tags %}
{% cryptpix_css %}
{% cryptpix_image photo width="100%" data-parent-size="true" %}
</code></pre>

<p>The <code>{% cryptpix_css %}</code> tag is required to ensure images render correctly, applying the essential styles for alignment and display. The <code>{% cryptpix_image %}</code> tag supports flexible options like responsive sizing and custom attributes, allowing you to tailor the display to your site’s design. Once integrated, CryptPix automatically processes images upon upload, storing the necessary data to render them securely. The Django admin interface includes previews and metadata for easy verification, ensuring developers can manage protected images with confidence.</p>

<h3 id="use-cases-benefits">Use Cases and Benefits</h3>

<p>CryptPix is a game-changer for any website that relies on visual content. E-commerce platforms can protect product images from competitors looking to scrape catalogs. Photographers and artists can safeguard high-resolution portfolios from unauthorized reproduction. News outlets can secure exclusive graphics, while educational platforms can shield proprietary diagrams and illustrations. In each case, CryptPix ensures that your images remain a valuable asset exclusive to your site, deterring theft without impacting the user experience.</p>

<p>The benefits extend beyond security. By automating the protection process, CryptPix saves developers time and effort, integrating seamlessly into existing workflows. Its responsive design support ensures images look great on any device, while its lightweight implementation avoids performance bottlenecks. Most importantly, it provides peace of mind: even if a scraper bypasses one layer of defense, the resulting image is a scrambled puzzle, useless for any practical purpose.</p>

<h3 id="why-choose-cryptpix">Why Choose CryptPix?</h3>

<p>CryptPix isn’t just another anti-scraping tool—it’s a strategic advantage for any site owner or developer serious about protecting visual content. Its multi-layered defenses outsmart both automated bots and manual scrapers, offering a level of security that other solutions can’t match. Unlike clunky alternatives that rely on visible watermarks or restrictive access controls, CryptPix delivers invisible, robust protection that preserves the beauty of your images. Its open-source foundation fosters community-driven innovation, ensuring it stays ahead of evolving threats. For developers, its Django integration is a dream, requiring minimal setup to achieve maximum impact—starting with the essential <code>{% cryptpix_css %}</code> tag. For site owners, it’s a promise that your images are safe, accessible only to your intended audience.</p>

<p>Join the growing community of developers and businesses using CryptPix to protect their visual assets. Install it today, explore the documentation, and discover why CryptPix is the smarter, stronger way to keep your images secure.</p>

<h1 id="cryptpix-installation-integration">CryptPix Installation and Integration Instructions</h1>

<p><strong>CryptPix</strong> is a Django package that provides a minimal image obfuscation tool. It splits images into layered components for CSS-based reconstruction, enhancing image protection in your Django application by serving them through secure, signed URLs.</p>

<h3 id="installation">Installation</h3>

<p>To install the cryptpix package, run the following command in your terminal:</p>

<pre><code class="language-bash">pip install git+https://github.com/ArtoLabs/CryptPix.git</code></pre>

<h4 id="requirements">Requirements</h4>

<ul>
  <li>Python: Version 3.7 or later</li>
  <li>Django: Version 3.0 or later</li>
  <li>Pillow: Required for image processing</li>
</ul>

<p>Install Pillow if it’s not already in your environment:</p>

<pre><code class="language-bash">pip install Pillow</code></pre>

<h4 id="system-dependencies">System Dependencies</h4>

<p>Pillow may require additional system dependencies, such as <code>libjpeg</code>, to handle image processing. Ensure these are installed on your system. Refer to the Pillow documentation for platform-specific installation instructions.</p>

<p><strong>For example:</strong></p>

<ul>
  <li>On Ubuntu: <code>sudo apt-get install libjpeg-dev</code></li>
  <li>On macOS: <code>brew install libjpeg</code></li>
</ul>

<h3 id="setup-django-project">Setup in Django Project</h3>

<h4 id="add-installed-apps">Add to INSTALLED_APPS</h4>

<p>Open your project’s <code>settings.py</code> file and add <code>'cryptpix'</code> to the <code>INSTALLED_APPS</code> list:</p>

<pre><code class="language-python">INSTALLED_APPS = [
    ...
    'cryptpix.apps.CryptPixConfig',
]</code></pre>

<h4 id="configure-urls">Configure URLs</h4>

<p>Include the <code>cryptpix</code> URL configuration in your project’s <code>urls.py</code>:</p>

<pre><code class="language-python">from django.urls import path, include

urlpatterns = [
    ...
    path('cryptpix/', include('cryptpix.urls')),
]</code></pre>

<p>This sets up the <code>secure_image_view</code> at <code>/cryptpix/secure-image/&lt;signed_value&gt;/</code>, which serves the protected image layers.</p>

<h4 id="handle-static-files">Handle Static Files</h4>

<p>The <code>cryptpix</code> package includes a JavaScript file (<code>resize_image_stacks.js</code>) required for responsive image resizing with the <code>breakpoints</code> attribute. To make it available, ensure your project is configured to serve static files:</p>

<p>In <code>settings.py</code>, verify that <code>STATIC_URL</code> is defined (e.g., <code>STATIC_URL = '/static/'</code>) and that <code>STATICFILES_DIRS</code> or <code>STATIC_ROOT</code> is set up for your project.</p>

<p>Run the following command to collect static files:</p>

<pre><code class="language-bash">python manage.py collectstatic</code></pre>

<p>Ensure the <code>{% load static %}</code> tag is used in templates to reference static files (see <em>Template Tags</em>).</p>

<h4 id="include-css-javascript">Include CSS and JavaScript</h4>

<p>Add the <code>{% cryptpix_css %}</code> tag in your template’s <code>&lt;head&gt;</code> section to include the necessary CSS for layer reconstruction:</p>

<pre><code class="language-django">{% cryptpix_css %}</code></pre>

<p>Include the <code>resize_image_stacks.js</code> script on pages that use the <code>{% cryptpix_image %}</code> tag:</p>

<pre><code class="language-html">&lt;script src="{% static 'cryptpix/resize_image_stacks.js' %}"&gt;&lt;/script&gt;</code></pre>

<p><strong>Important:</strong> The JavaScript file is required to dynamically adjust image sizes. Place it in the <code>&lt;body&gt;</code> or <code>&lt;head&gt;</code> section of your template, ensuring <code>{% load static %}</code> is included.</p>

<h4 id="run-migrations">Run Migrations</h4>

<p>Run migrations to create the necessary database fields:</p>

<pre><code class="language-bash">python manage.py migrate</code></pre>

<p>No additional middleware, template tags, or static files are required beyond what’s described below.</p>

<h3 id="using-cryptpix-model-mixin">Using the CryptPix Model Mixin</h3>

<h4 id="adding-mixin">Adding the Mixin</h4>

<p>Add <code>CryptPixModelMixin</code> to the model containing the image field you want to protect. By default, the mixin assumes the image field is named <code>'image'</code>. This is controlled by the <code>cryptpix_source_field</code> attribute.</p>

<h4 id="configuring-source-field">Important: Configuring the Source Field</h4>

<p>If your image field is named anything other than <code>'image'</code>, override <code>cryptpix_source_field</code> to match your field’s name.</p>

<h4 id="example-model">Example Model</h4>

<pre><code class="language-python">from django.db import models
from cryptpix.django import CryptPixModelMixin

class MyModel(CryptPixModelMixin, models.Model):
    image = models.ImageField(upload_to='images/')

    # Default: cryptpix_source_field = 'image'
    # If your field is named differently, e.g., 'photo', override it:
    # cryptpix_source_field = 'photo'
</code></pre>

<p>In this example, since the field is named <code>'image'</code>, no override is needed.</p>

<h4 id="what-happens">What Happens</h4>

<p>When the model instance is saved with an image, the mixin:</p>

<ul>
  <li>Distorts the image.</li>
  <li>Splits it into two layers.</li>
  <li>Stores these layers in the database, along with metadata.</li>
</ul>

<p>The original image remains in the source field unless you restrict access (see next section).</p>



<h2 id="security-modes-and-rendering-architecture">Security Modes and Rendering Architecture</h2>

<p>CryptPix supports three distinct security behaviors. Each mode builds on the previous one, increasing protection while preserving a stable DOM contract for consuming projects.</p>

<p>All three modes share the same outer wrapper element and class structure. Every rendered image is wrapped in:</p>

<ul>
  <li><code>&lt;div class="image-stack"&gt;</code></li>
  <li>A <code>data-layout</code> attribute indicating <code>"single"</code> or <code>"stack"</code></li>
  <li>Consistent <code>data-natural-width</code> and <code>data-natural-height</code> attributes when available</li>
</ul>

<p>This guarantees that CSS selectors and JavaScript integrations can rely on a stable container contract, regardless of how many <code>&lt;img&gt;</code> elements are rendered internally.</p>

<hr>

<h3 id="mode-1-secure-single-image-obfuscated-link">Mode 1: Secure Single Image (Obfuscated Link)</h3>

<p><strong>What it does</strong></p>

<ul>
  <li>Stores one processed PNG derivative in <code>image_layer_1</code>.</li>
  <li>Serves it through a short-lived, signed URL tied to the user’s session.</li>
  <li>Renders a single <code>&lt;img&gt;</code> element in the DOM.</li>
  <li>Uses lazy loading with a placeholder <code>src</code> and a signed <code>data-src</code>.</li>
</ul>

<p>No visual distortion or splitting occurs. Protection is provided through controlled delivery and expiring, session-bound URLs.</p>

<p><strong>DOM Output</strong></p>

<p>This mode renders exactly <strong>one <code>&lt;img&gt;</code> element</strong> inside the wrapper.</p>

<pre><code>&lt;div class="image-stack" data-layout="single" data-natural-width="1200" data-natural-height="800"&gt;
  &lt;img
    src="data:image/gif;base64,..."
    data-src="/cryptpix/secure-image/&lt;signed_value&gt;/"
    loading="lazy"
    class="lazy"
    data-natural-width="1200"
    data-natural-height="800"&gt;
&lt;/div&gt;
</code></pre>

<p><strong>When to use</strong></p>

<ul>
  <li>When you want link protection without visual transformation.</li>
  <li>When maintaining pixel-perfect original color data is important.</li>
  <li>When minimal processing overhead is preferred.</li>
</ul>

<hr>

<h3 id="mode-2-secure-single-image-with-visual-distortion">Mode 2: Secure Single Image with Visual Distortion</h3>

<p><strong>What it does</strong></p>

<ul>
  <li>Applies hue rotation and color inversion at save time.</li>
  <li>Stores the distorted image in <code>image_layer_1</code>.</li>
  <li>Persists the chosen <code>hue_rotation</code> value.</li>
  <li>Reverses the distortion in the browser using an inline CSS filter.</li>
  <li>Still renders a single <code>&lt;img&gt;</code> element.</li>
</ul>

<p>The image stored on disk is visually altered. Only when rendered inside the CryptPix wrapper with the correct filter does it appear normal.</p>

<p><strong>DOM Output</strong></p>

<p>This mode also renders exactly <strong>one <code>&lt;img&gt;</code> element</strong>, identical in structure to Mode 1, but with a reversing CSS filter applied inline.</p>

<pre><code>&lt;div class="image-stack" data-layout="single" data-natural-width="1200" data-natural-height="800"&gt;
  &lt;img
    src="data:image/gif;base64,..."
    data-src="/cryptpix/secure-image/&lt;signed_value&gt;/"
    loading="lazy"
    class="lazy"
    style="filter: invert(100%) hue-rotate(-120deg);"
    data-natural-width="1200"
    data-natural-height="800"&gt;
&lt;/div&gt;
</code></pre>

<p><strong>How it differs from Mode 1</strong></p>

<ul>
  <li>Same DOM structure.</li>
  <li>Same single-image rendering.</li>
  <li>Additional pixel-level transformation stored on disk.</li>
  <li>Inline CSS filter reverses the transformation at render time.</li>
</ul>

<p><strong>When to use</strong></p>

<ul>
  <li>When you want stronger protection against raw file reuse.</li>
  <li>When you want downloaded derivatives to appear visually incorrect outside your site.</li>
  <li>When you still prefer a simple single-image DOM structure.</li>
</ul>

<hr>

<h3 id="mode-3-secure-split-layer-reconstruction">Mode 3: Secure Split-Layer Reconstruction</h3>

<p><strong>What it does</strong></p>

<ul>
  <li>Optionally distorts the image first.</li>
  <li>Splits the image into a checkerboard pattern.</li>
  <li>Stores two separate PNG derivatives: <code>image_layer_1</code> and <code>image_layer_2</code>.</li>
  <li>Persists <code>tile_size</code>, <code>image_width</code>, and <code>image_height</code>.</li>
  <li>Renders two coordinated <code>&lt;img&gt;</code> elements stacked in the same container.</li>
  <li>Reconstructs the full image visually in the browser.</li>
</ul>

<p>Each layer contains alternating tiles. Individually, they are incomplete. Only when stacked in the browser do they form the full image.</p>

<p><strong>DOM Output</strong></p>

<p>This mode renders <strong>two <code>&lt;img&gt;</code> elements</strong> inside the same <code>.image-stack</code> wrapper, plus hidden metadata used for layout.</p>

<pre><code>&lt;div class="image-stack" data-layout="stack" data-natural-width="1200" data-natural-height="800"&gt;
  &lt;img
    src="data:image/gif;base64,..."
    data-src="/cryptpix/secure-image/&lt;signed_value_layer1&gt;/"
    loading="lazy"
    class="lazy"
    style="filter: invert(100%) hue-rotate(-120deg);"&gt;
  &lt;img
    src="data:image/gif;base64,..."
    data-src="/cryptpix/secure-image/&lt;signed_value_layer2&gt;/"
    loading="lazy"
    class="lazy"
    style="filter: invert(100%) hue-rotate(-120deg);"
    data-natural-width="1200"
    data-natural-height="800"&gt;
  &lt;div
    class="tile-meta"
    data-tile-size="24"
    data-breakpoints="[]"
    hidden&gt;
  &lt;/div&gt;
&lt;/div&gt;
</code></pre>

<p><strong>How it differs from Modes 1 and 2</strong></p>

<ul>
  <li>Renders two <code>&lt;img&gt;</code> elements instead of one.</li>
  <li>Requires layout coordination and tile quantization.</li>
  <li>Depends on JavaScript to calculate responsive stack dimensions.</li>
  <li>Introduces stored tiling metadata.</li>
</ul>

<p><strong>When to use</strong></p>

<ul>
  <li>When you want the strongest protection.</li>
  <li>When making downloaded image layers individually unusable is important.</li>
  <li>When accepting slightly more complexity in rendering and layout logic.</li>
</ul>

<hr>

<h2 id="stable-dom-contract">Stable DOM Contract</h2>

<p>Across all modes:</p>

<ul>
  <li>The outer wrapper is always <code>&lt;div class="image-stack"&gt;</code>.</li>
  <li>The <code>data-layout</code> attribute indicates <code>"single"</code> or <code>"stack"</code>.</li>
  <li>Natural dimension attributes are consistently exposed.</li>
  <li>The <code>&lt;img&gt;</code> elements always use lazy loading with <code>data-src</code>.</li>
  <li>The secure URL format and session validation remain identical.</li>
</ul>

<p>This guarantees that consuming projects can safely target:</p>

<p><code>.image-stack</code><br>
<code>.image-stack img.lazy</code></p>

<p>without needing to know which mode is active.</p>

<p>The only structural difference is the number of <code>&lt;img&gt;</code> elements inside the wrapper:</p>

<ul>
  <li>Modes 1 and 2: one <code>&lt;img&gt;</code></li>
  <li>Mode 3: two <code>&lt;img&gt;</code> elements</li>
</ul>

<hr>

<h2 id="css-integration-guidance">CSS Integration Guidance</h2>

<p>You must include the <code>{% cryptpix_css %}</code> tag in your <code>&lt;head&gt;</code> section. This ensures:</p>

<ul>
  <li>Proper positioning for split stacks.</li>
  <li>Normal flow layout for single-image mode.</li>
  <li>Correct lazy fade-in behavior.</li>
</ul>

<p>Do not override positioning rules for <code>.image-stack[data-layout="stack"] img</code>, as these rely on absolute stacking for visual reconstruction.</p>

<p>If you need custom styling, apply classes via the template tag and target the wrapper:</p>

<pre><code>{% cryptpix_image photo class="my-custom-image" width="100%" %}</code></pre>

<p>Then style <code>.my-custom-image</code> as needed, leaving the core stack behavior intact.</p>

<hr>

<h2 id="javascript-integration-guidance">JavaScript Integration Guidance</h2>

<p>If you use split-layer mode:</p>

<ul>
  <li>Include <code>resize_image_stacks.js</code>.</li>
  <li>Ensure it loads after the DOM is ready.</li>
  <li>Do not remove the <code>.tile-meta</code> element.</li>
</ul>

<p>The resizing script:</p>

<ul>
  <li>Selects only <code>.image-stack[data-layout="stack"]</code></li>
  <li>Ensures exactly two <code>&lt;img&gt;</code> elements are present</li>
  <li>Quantizes dimensions to tile multiples</li>
</ul>

<p>Single-image modes do not require the resizing logic, but can safely coexist with it because the script explicitly targets <code>data-layout="stack"</code>.</p>

<hr>

<p>By choosing the appropriate mode, you control the trade-off between simplicity and defensive strength. All modes preserve a stable rendering contract while scaling the depth of protection.</p>




<h1 id="integration-usage">Integration and Usage</h1>

<h2 id="template-tags">Template Tags</h2>

<h3 id="load-tags">Load the Tags</h3>
<p>In your Django template, load the <code>cryptpix_tags</code>:</p>

<pre><code class="language-django">{% load cryptpix_tags %}</code></pre>

<h3 id="render-protected-image">Render the Protected Image</h3>
<p>Use the <code>cryptpix_image</code> tag to display the protected image:</p>

<pre><code class="language-django">{% cryptpix_image my_model_instance %}</code></pre>

<p>Pass additional attributes to customize the display (applied to the top layer image). The <code>width</code> and <code>height</code> attributes can be specified in pixels (e.g., <code>"500px"</code>) or percentages (e.g., <code>"100%"</code>), but not as <code>"auto"</code>:</p>

<pre><code class="language-django">{% cryptpix_image my_model_instance width="500px" height="300px" class="my-class" %}</code></pre>

<p>or</p>

<pre><code class="language-django">{% cryptpix_image my_model_instance width="100%" height="50%" class="my-class" %}</code></pre>

<p><strong>Note:</strong> Using <code>height="auto"</code> is not supported, as it may break the CSS-based reconstruction of the layered images. Always specify a concrete value for <code>width</code> and <code>height</code>.</p>

<h3 id="using-breakpoints">Using Breakpoints</h3>

<p>The <code>breakpoints</code> attribute allows you to emulate CSS media queries by specifying different sizes for the image based on the viewport width. The <code>breakpoints</code> value is a JSON string defining viewport sizes and corresponding width and height values. This is useful for responsive designs.</p>

<p><strong>Example:</strong></p>

<pre><code class="language-django">{% cryptpix_image my_model_instance width="100%" height="50%" breakpoints='{"0": {"width": "100%", "height": "50%"}, "768": {"width": "500px", "height": "300px"}}' %}</code></pre>

<h4 id="explanation-breakpoints">Explanation:</h4>
<p>The <code>breakpoints</code> JSON object maps minimum viewport widths (in pixels) to an object containing <code>width</code> and <code>height</code> values.</p>

<p>In the example above:</p>
<ul>
  <li>For viewports narrower than <code>768px</code>, the image uses <code>width="100%"</code> and <code>height="50%"</code>.</li>
  <li>For viewports <code>768px</code> or wider, the image uses <code>width="500px"</code> and <code>height="300px"</code>.</li>
</ul>

<p>The breakpoints emulate CSS media queries by dynamically adjusting the image size based on the client’s viewport.</p>

<h4 id="use-breakpoints-effectively">To use breakpoints effectively:</h4>
<ul>
  <li>Ensure the JSON is valid and properly formatted.</li>
  <li>Use pixel or percentage values for <code>width</code> and <code>height</code> within the breakpoints, consistent with the main <code>width</code> and <code>height</code> attributes.</li>
  <li>Test across different screen sizes to verify responsiveness.</li>
</ul>

<h5 id="include-css">Include CSS</h5>

<p>Add in your template’s <code>&lt;head&gt;</code>. This step is required for the images to render correctly:</p>

<pre><code class="language-django">{% cryptpix_css %}</code></pre>

<h4 id="how-image-served">How the Image Is Served</h4>

<ul>
  <li>Signed URLs for <code>image_layer_1</code> and <code>image_layer_2</code> (default valid for 5 seconds).</li>
  <li>Secure view checks against the user's session.</li>
  <li>Layers are stacked via CSS. The original image is not served unless manually exposed.</li>
</ul>

<h4 id="protecting-original-image">Protecting the Original Image</h4>

<p><strong>Important:</strong> Do <em>not</em> use <code>{{ my_model_instance.image.url }}</code>. Always use <code>{% cryptpix_image %}</code>.</p>

<p>Optionally, configure a private directory or custom storage backend.</p>

<h3 id="generating-secure-url">Generating a Secure URL for the Original Image</h3>

<p>In cases where you cannot use the <code>{% cryptpix_image %}</code> template tag (e.g., when passing an image URL to a third-party JavaScript application that does not support the CryptPix HTML snippet), you can use the <code>get_secure_image_url</code> function to generate a short-lived, secure URL for the original image. This approach bypasses the CryptPix distortion layers but still provides protection through a signed, ephemeral URL that prevents scraping.</p>

<p><strong>Example Usage in a View:</strong></p>

<pre><code class="language-python">from cryptpix.html import get_secure_image_url

def my_view(request):
    title_media = MyModel.objects.get(pk=1)  # Example model instance
    image_pk = str(title_media.media.pk) + '_0' if title_media and title_media.media else None
    media_url = get_secure_image_url(image_pk, request) if image_pk else None
    return render(request, 'my_template.html', {'media_url': media_url})
</code></pre>

<p><strong>Explanation:</strong></p>
<ul>
  <li>The <code>image_pk</code> is constructed by appending <code>'_0'</code> to the model instance’s primary key (e.g., <code>media.pk</code>). This ensures the original image is retrieved instead of the distorted layers.</li>
  <li>The <code>get_secure_image_url</code> function generates a signed URL tied to the user’s session, which expires quickly (default: 5 seconds) to prevent unauthorized access or scraping.</li>
  <li>Use this URL in contexts where a direct image URL is required, such as passing it to a third-party JavaScript library.</li>
</ul>

<p><strong>Template Usage:</strong></p>
<p>Pass the generated URL to your template and use it in an <code>&lt;img&gt;</code> tag or JavaScript code:</p>

<pre><code class="language-html">&lt;img src="{{ media_url }}" alt="Protected Image"&gt;
</code></pre>

<p><strong>Important Notes:</strong></p>
<ul>
  <li>Always append <code>'_0'</code> to the image’s primary key to retrieve the original image.</li>
  <li>The generated URL is short-lived, providing a layer of protection against scraping, even without the CryptPix distortion layers.</li>
  <li>Avoid exposing the original image’s storage path (e.g., <code>{{ object.image.url }}</code>) to maintain security.</li>
</ul>

<h3 id="configuration-options">Configuration Options</h3>

<ul>
  <li><strong>Signed URL Expiry:</strong> Set <code>max_age</code> in <code>unsign_image_token</code> (default: 5s).</li>
  <li><strong>Image Processing:</strong> Modify <code>choose_tile_size</code> or <code>distort_image</code> in <code>core.py</code>.</li>
  <li><strong>Template Attributes:</strong> Pass <code>width</code>, <code>height</code>, <code>class</code>, etc.</li>
</ul>

<h3 id="running-testing">Running and Testing</h3>

<h4 id="running-server">Running the Server</h4>

<pre><code class="language-bash">python manage.py runserver</code></pre>

<p>Navigate to a page using the <code>{% cryptpix_image %}</code> tag.</p>

<h4 id="example-setup">Example Setup</h4>

<p><strong>View:</strong></p>

<pre><code class="language-python">from django.views.generic import DetailView
from .models import MyModel

class MyModelDetailView(DetailView):
    model = MyModel
    template_name = 'my_model_detail.html'
</code></pre>

<p><strong>URL:</strong></p>

<pre><code class="language-python">from django.urls import path
from .views import MyModelDetailView

urlpatterns = [
    path('mymodel/&lt;int:pk&gt;/', MyModelDetailView.as_view(), name='mymodel-detail'),
]</code></pre>

<p><strong>Template (my_model_detail.html):</strong></p>

<pre><code class="language-html">&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
    {% cryptpix_css %}
&lt;/head&gt;
&lt;body&gt;
    {% load cryptpix_tags %}
    {% cryptpix_image object width="100%" %}
&lt;/body&gt;
&lt;/html&gt;
</code></pre>

<p><strong>Visit:</strong> <code>/mymodel/1/</code> (assuming <code>pk=1</code> exists).</p>

<h4 id="verifying-works">Verifying It Works</h4>

<ul>
  <li><strong>Image Display:</strong> Should render with layered protection.</li>
  <li><strong>Protection Check:</strong> Direct access to layer URLs should fail after expiration or with an invalid session.</li>
  <li><strong>Original Image:</strong> Remains accessible unless protected.</li>
</ul>

<h3 id="admin-previews">Admin Previews</h3>

<p>Use <code>CryptPixAdminMixin</code> for previews:</p>

<pre><code class="language-python">from django.contrib import admin
from cryptpix.admin import CryptPixAdminMixin
from .models import MyModel

@admin.register(MyModel)
class MyModelAdmin(CryptPixAdminMixin, admin.ModelAdmin):
    list_display = ['id', 'display_thumbnail']
    readonly_fields = (
        'image_layer_1_preview',
        'image_layer_2_preview',
        'tile_size',
        'image_width',
        'image_height',
        'hue_rotation',
    )
</code></pre>

<p>Visit the admin interface to see thumbnails and layer previews.</p>

<h3 id="troubleshooting-tips">Troubleshooting Tips</h3>

<ul>
  <li><strong>Image Not Displaying:</strong> Check <code>cryptpix_source_field</code>.</li>
  <li><strong>CSS Missing:</strong> Ensure <code>{% cryptpix_css %}</code> is in <code>&lt;head&gt;</code>.</li>
  <li><strong>Migrations:</strong> Run <code>python manage.py migrate</code> if fields are missing.</li>
  <li><strong>Image Processing Fails:</strong> Ensure Pillow and dependencies like libjpeg are installed.</li>
  <li><strong>URL Errors:</strong> Confirm <code>path('cryptpix/', include(...))</code> is present.</li>
  <li><strong>Original Image Exposed:</strong> Avoid <code>{{ object.image.url }}</code>.</li>
  <li><strong>Signed URL Issues:</strong> Check session validity and <code>max_age</code> settings.</li>
</ul>