#!/usr/bin/env python3
"""Website generation module for JARVIS Pro."""

import json
import logging
from typing import Dict, List, Optional
from enum import Enum
import os

logger = logging.getLogger(__name__)


class WebsiteType(Enum):
    """Types of websites to generate."""
    PORTFOLIO = "portfolio"
    BUSINESS = "business"
    ECOMMERCE = "ecommerce"
    BLOG = "blog"
    DASHBOARD = "dashboard"
    ADMIN_PANEL = "admin_panel"
    LANDING_PAGE = "landing_page"
    SPA = "spa"


class WebsiteGenerator:
    """Generate complete websites from prompts."""

    def __init__(self, ai_agent):
        """Initialize website generator with AI agent."""
        self.ai_agent = ai_agent
        self.websites_generated: List[Dict] = []

    def generate_website(self, prompt: str, website_type: WebsiteType, 
                        use_tailwind: bool = True) -> Dict[str, str]:
        """Generate a complete website with HTML, CSS, JavaScript."""
        try:
            logger.info(f"Generating {website_type.value} website")
            
            # Generate HTML
            html = self._generate_html(prompt, website_type)
            
            # Generate CSS
            css = self._generate_css(prompt, website_type, use_tailwind)
            
            # Generate JavaScript
            js = self._generate_javascript(prompt, website_type)
            
            website = {
                "type": website_type.value,
                "html": html,
                "css": css,
                "javascript": js,
                "prompt": prompt,
                "use_tailwind": use_tailwind
            }
            
            self.websites_generated.append(website)
            logger.info(f"Website generated successfully")
            
            return website
        except Exception as e:
            logger.error(f"Error generating website: {e}")
            return {"error": str(e)}

    def _generate_html(self, prompt: str, website_type: WebsiteType) -> str:
        """Generate HTML structure."""
        try:
            type_desc = website_type.value.replace("_", " ")
            ai_prompt = f"""Generate HTML for a {type_desc} website based on: {prompt}
            
Requirements:
1. Semantic HTML5 structure
2. Responsive meta viewport
3. Accessibility features (ARIA)
4. SEO meta tags
5. Clean structure
6. Return ONLY the HTML code
7. Include <html>, <head>, <body> tags"""

            html = self.ai_agent.ask(ai_prompt)
            return html
        except Exception as e:
            logger.error(f"Error generating HTML: {e}")
            return f"<!-- Error: {e} -->"

    def _generate_css(self, prompt: str, website_type: WebsiteType, 
                     use_tailwind: bool) -> str:
        """Generate CSS styling."""
        try:
            type_desc = website_type.value.replace("_", " ")
            css_framework = "Tailwind CSS" if use_tailwind else "modern CSS"
            
            ai_prompt = f"""Generate {css_framework} for a {type_desc} website: {prompt}
            
Requirements:
1. Responsive design (mobile-first)
2. Modern styling
3. Dark mode support
4. Smooth animations
5. Professional appearance
6. {'Use Tailwind CSS classes' if use_tailwind else 'Use vanilla CSS'}
7. Return ONLY the CSS/styles code"""

            css = self.ai_agent.ask(ai_prompt)
            return css
        except Exception as e:
            logger.error(f"Error generating CSS: {e}")
            return f"/* Error: {e} */"

    def _generate_javascript(self, prompt: str, website_type: WebsiteType) -> str:
        """Generate JavaScript functionality."""
        try:
            type_desc = website_type.value.replace("_", " ")
            ai_prompt = f"""Generate modern JavaScript for a {type_desc} website: {prompt}
            
Requirements:
1. ES6+ syntax
2. Event handlers
3. Interactive features
4. Form handling (if applicable)
5. Smooth interactions
6. No external dependencies (vanilla JS)
7. Return ONLY the JavaScript code
8. Include error handling"""

            js = self.ai_agent.ask(ai_prompt)
            return js
        except Exception as e:
            logger.error(f"Error generating JavaScript: {e}")
            return f"// Error: {e}"

    def generate_portfolio_website(self, name: str, skills: List[str], 
                                   projects: List[str]) -> Dict[str, str]:
        """Generate a portfolio website."""
        prompt = f"""Create a professional portfolio website for {name}.
        
Skills: {', '.join(skills)}
Projects: {', '.join(projects)}

Include:
1. Hero section with introduction
2. Skills showcase
3. Project portfolio
4. Contact form
5. Dark mode toggle"""
        
        return self.generate_website(prompt, WebsiteType.PORTFOLIO)

    def generate_business_website(self, company_name: str, services: List[str]) -> Dict[str, str]:
        """Generate a business website."""
        prompt = f"""Create a professional business website for {company_name}.
        
Services: {', '.join(services)}

Include:
1. Company overview
2. Services section
3. Team member showcase
4. Testimonials
5. Contact/booking form"""
        
        return self.generate_website(prompt, WebsiteType.BUSINESS)

    def generate_ecommerce_website(self, store_name: str, products: List[str]) -> Dict[str, str]:
        """Generate an e-commerce website."""
        prompt = f"""Create an e-commerce website for {store_name}.
        
Products: {', '.join(products)}

Include:
1. Product catalog
2. Shopping cart
3. Product filters
4. Product details
5. Checkout form
6. Payment integration info"""
        
        return self.generate_website(prompt, WebsiteType.ECOMMERCE)

    def generate_blog(self, blog_name: str, topics: List[str]) -> Dict[str, str]:
        """Generate a blog website."""
        prompt = f"""Create a blog website called {blog_name}.
        
Main topics: {', '.join(topics)}

Include:
1. Blog post list
2. Featured posts
3. Search functionality
4. Categories
5. Comments section
6. Newsletter signup"""
        
        return self.generate_website(prompt, WebsiteType.BLOG)

    def generate_dashboard(self, dashboard_name: str, data_types: List[str]) -> Dict[str, str]:
        """Generate a dashboard website."""
        prompt = f"""Create a dashboard for {dashboard_name}.
        
Data to display: {', '.join(data_types)}

Include:
1. Header with user info
2. Sidebar navigation
3. Analytics widgets
4. Charts and graphs
5. Data tables
6. Real-time updates UI"""
        
        return self.generate_website(prompt, WebsiteType.DASHBOARD)

    def save_website(self, website: Dict[str, str], output_dir: str) -> bool:
        """Save website files to disk."""
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            # Save HTML
            html_path = os.path.join(output_dir, "index.html")
            with open(html_path, "w") as f:
                f.write(website.get("html", ""))
            
            # Save CSS
            css_path = os.path.join(output_dir, "style.css")
            with open(css_path, "w") as f:
                f.write(website.get("css", ""))
            
            # Save JavaScript
            js_path = os.path.join(output_dir, "script.js")
            with open(js_path, "w") as f:
                f.write(website.get("javascript", ""))
            
            logger.info(f"Website saved to {output_dir}")
            return True
        except Exception as e:
            logger.error(f"Error saving website: {e}")
            return False

    def get_generated_websites(self) -> List[Dict]:
        """Get list of generated websites."""
        return self.websites_generated
