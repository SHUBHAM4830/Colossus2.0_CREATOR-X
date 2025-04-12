document.addEventListener('DOMContentLoaded', function() {
    // Initialize language
    const currentLang = localStorage.getItem('preferredLanguage') || 'en';
    setLanguage(currentLang);
    document.getElementById('language-input').value = currentLang;
    
    // Language button event listeners
    const langButtons = document.querySelectorAll('.lang-btn');
    langButtons.forEach(button => {
        if(button.dataset.lang === currentLang) {
            button.classList.add('active');
        }
        
        button.addEventListener('click', function() {
            const lang = this.dataset.lang;
            setLanguage(lang);
            
            // Update active class
            langButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Update hidden input
            document.getElementById('language-input').value = lang;
            
            // Save preference
            localStorage.setItem('preferredLanguage', lang);
        });
    });
    
    // Show result section if there's a prediction
    const resultSection = document.getElementById('result-section');
    if(resultSection.querySelector('.crop-name')?.textContent.trim()) {
        resultSection.classList.add('active');
    }
    
    // Form validation
    const cropForm = document.getElementById('crop-form');
    if(cropForm) {
        cropForm.addEventListener('submit', function(e) {
            const isValid = validateForm();
            if(!isValid) {
                e.preventDefault();
            }
        });
    }
    
    // Input validation functions
    function validateForm() {
        let isValid = true;
        
        // pH validation (0-14)
        const phInput = document.getElementById('ph');
        const phValue = parseFloat(phInput.value);
        if(isNaN(phValue) || phValue < 0 || phValue > 14) {
            highlightError(phInput, getTranslation('ph_error'));
            isValid = false;
        } else {
            removeError(phInput);
        }
        
        // All inputs should be positive
        const numberInputs = document.querySelectorAll('input[type="number"]');
        numberInputs.forEach(input => {
            if(input.id !== 'ph') { // pH already validated
                const value = parseFloat(input.value);
                if(isNaN(value) || value < 0) {
                    highlightError(input, getTranslation('positive_number_error'));
                    isValid = false;
                } else {
                    removeError(input);
                }
            }
        });
        
        return isValid;
    }
    
    function highlightError(inputElement, message) {
        // Remove any existing error message
        removeError(inputElement);
        
        // Add error class and message
        inputElement.classList.add('error-input');
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        inputElement.parentNode.appendChild(errorDiv);
    }
    
    function removeError(inputElement) {
        inputElement.classList.remove('error-input');
        const existingError = inputElement.parentNode.querySelector('.error-message');
        if(existingError) {
            existingError.remove();
        }
    }
    
    // Language handling functions
    function setLanguage(lang) {
        const elements = document.querySelectorAll('[data-i18n]');
        elements.forEach(element => {
            const key = element.getAttribute('data-i18n');
            element.textContent = getTranslation(key, lang);
        });
        
        // Update document direction for RTL languages if needed
        // document.dir = lang === 'ar' ? 'rtl' : 'ltr';
    }
    
    function getTranslation(key, lang = null) {
        if(!lang) {
            lang = document.getElementById('language-input').value;
        }
        
        if(translations[lang] && translations[lang][key]) {
            return translations[lang][key];
        }
        
        // Fallback to English
        return translations['en'][key] || key;
    }
});

// Translations
const translations = {
    'en': {
        'page_title': 'Crop Recommendation System',
        'main_heading': 'Crop Recommendation System',
        'form_heading': 'Enter Soil and Climate Data',
        'nitrogen': 'Nitrogen (N):',
        'phosphorus': 'Phosphorus (P):',
        'potassium': 'Potassium (K):',
        'temperature': 'Temperature:',
        'humidity': 'Humidity:',
        'ph': 'pH:',
        'rainfall': 'Rainfall:',
        'submit_btn': 'Get Recommendation',
        'result_heading': 'Recommended Crop',
        'crop_recommendation': 'Based on your input, the recommended crop is:',
        'footer_text': '© 2025 Crop Recommendation System',
        'ph_error': 'pH value must be between 0 and 14',
        'positive_number_error': 'Please enter a positive number'
    },
    'hi': {
        'page_title': 'फसल अनुशंसा प्रणाली',
        'main_heading': 'फसल अनुशंसा प्रणाली',
        'form_heading': 'मिट्टी और जलवायु डेटा दर्ज करें',
        'nitrogen': 'नाइट्रोजन (N):',
        'phosphorus': 'फॉस्फोरस (P):',
        'potassium': 'पोटेशियम (K):',
        'temperature': 'तापमान:',
        'humidity': 'आर्द्रता:',
        'ph': 'पीएच:',
        'rainfall': 'वर्षा:',
        'submit_btn': 'अनुशंसा प्राप्त करें',
        'result_heading': 'अनुशंसित फसल',
        'crop_recommendation': 'आपके इनपुट के आधार पर, अनुशंसित फसल है:',
        'footer_text': '© 2025 फसल अनुशंसा प्रणाली',
        'ph_error': 'पीएच मान 0 और 14 के बीच होना चाहिए',
        'positive_number_error': 'कृपया एक सकारात्मक संख्या दर्ज करें'
    },
    'kn': {
        'page_title': 'ಬೆಳೆ ಶಿಫಾರಸು ವ್ಯವಸ್ಥೆ',
        'main_heading': 'ಬೆಳೆ ಶಿಫಾರಸು ವ್ಯವಸ್ಥೆ',
        'form_heading': 'ಮಣ್ಣು ಮತ್ತು ಹವಾಮಾನ ಡೇಟಾವನ್ನು ನಮೂದಿಸಿ',
        'nitrogen': 'ಸಾರಜನಕ (N):',
        'phosphorus': 'ರಂಜಕ (P):',
        'potassium': 'ಪೊಟ್ಯಾಸಿಯಂ (K):',
        'temperature': 'ತಾಪಮಾನ:',
        'humidity': 'ಆರ್ದ್ರತೆ:',
        'ph': 'ಪಿಎಚ್:',
        'rainfall': 'ಮಳೆ:',
        'submit_btn': 'ಶಿಫಾರಸನ್ನು ಪಡೆಯಿರಿ',
        'result_heading': 'ಶಿಫಾರಸು ಮಾಡಿದ ಬೆಳೆ',
        'crop_recommendation': 'ನಿಮ್ಮ ಇನ್‌ಪುಟ್ ಆಧಾರದ ಮೇಲೆ, ಶಿಫಾರಸು ಮಾಡಿದ ಬೆಳೆ:',
        'footer_text': '© 2025 ಬೆಳೆ ಶಿಫಾರಸು ವ್ಯವಸ್ಥೆ',
        'ph_error': 'ಪಿಎಚ್ ಮೌಲ್ಯವು 0 ಮತ್ತು 14 ನಡುವೆ ಇರಬೇಕು',
        'positive_number_error': 'ದಯವಿಟ್ಟು ಧನಾತ್ಮಕ ಸಂಖ್ಯೆಯನ್ನು ನಮೂದಿಸಿ'
    }
};