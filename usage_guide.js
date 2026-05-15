document.addEventListener('DOMContentLoaded', () => {
    // Calculator Logic
    const volumeInput = document.getElementById('volume-input');
    const resultValue = document.getElementById('dosage-result');
    const productType = document.getElementById('product-type');
    const packagingSuggestion = document.getElementById('packaging-suggestion');
    let currentProdLine = 'liquid';

    function calculateDosage() {
        const volume = parseFloat(volumeInput.value) || 0;
        let dosage = 0;
        let unit = '';
        let suggestion = '';

        if (currentProdLine === 'liquid') {
            unit = 'ลิตร (L)';
            if (productType.value === 'trap') {
                // Formula: 1L per 10 m3
                dosage = volume * 0.1;
            } else {
                // Formula: 50ml per point
                dosage = volume * 0.05;
            }
            dosage = dosage.toFixed(2);
            
            // Suggestion
            if (dosage <= 1) suggestion = 'แนะแนวทาง: ใช้แกลลอนขนาด 1 L';
            else if (dosage <= 5) suggestion = 'แนะแนวทาง: ใช้แกลลอนขนาด 5 L';
            else suggestion = `แนะแนวทาง: ใช้แกลลอน 5 L จำนวน ${Math.ceil(dosage / 5)} แกลลอน`;

        } else { // Premium
            if (productType.value === 'trap') {
                unit = 'กิโลกรัม (kg)';
                // Formula: 1kg per 10 m3
                dosage = volume * 0.1;
                dosage = dosage.toFixed(2);

                if (dosage <= 1) suggestion = 'แนะแนวทาง: ใช้สูตรพรีเมียมถุง 1 kg';
                else if (dosage <= 6) suggestion = 'แนะแนวทาง: ใช้สูตรพรีเมียมถัง 6 kg';
                else suggestion = `แนะแนวทาง: ใช้ถัง 6 kg จำนวน ${Math.ceil(dosage / 6)} ถัง`;
            } else {
                unit = 'ซอง (Tea Bag)';
                // Formula: 1 bag per point
                dosage = volume;
                suggestion = `แนะแนวทาง: ใช้รุ่นซองชา จำนวน ${Math.ceil(dosage / 6)} ถุง (บรรจุ 6 ซอง/ถุง)`;
            }
        }

        resultValue.innerText = `${dosage} ${unit}`;
        packagingSuggestion.innerText = suggestion;
    }

    volumeInput.addEventListener('input', calculateDosage);
    productType.addEventListener('change', () => {
        const label = document.getElementById('input-label');
        const unitLabel = document.getElementById('input-unit');
        
        if (productType.value === 'trap') {
            label.innerText = 'ขนาดบ่อบำบัด / บ่อดักไขมัน';
            unitLabel.innerText = 'm³';
            volumeInput.placeholder = 'ระบุจำนวนลูกบาศก์เมตร';
        } else {
            label.innerText = 'จำนวนจุดระบายน้ำ / ซิงค์ล้างจาน';
            unitLabel.innerText = 'จุด';
            volumeInput.placeholder = 'ระบุจำนวนจุด';
        }
        calculateDosage();
    });

    // Tab Switching Logic (Product Line and Guides)
    const allTabBtns = document.querySelectorAll('.tab-btn');
    
    allTabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const prodLine = btn.getAttribute('data-prod-line');
            const guideId = btn.getAttribute('data-tab');

            if (prodLine) {
                // Product Line Selection
                document.querySelectorAll('[data-prod-line]').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentProdLine = prodLine;
                
                // Update Info Blocks
                document.querySelectorAll('.prod-info-block').forEach(block => block.style.display = 'none');
                document.getElementById(`info-${prodLine}`).style.display = 'block';
                
                calculateDosage();
            } else if (guideId) {
                // Usage Guide Tabs
                document.querySelectorAll('[data-tab]').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
                document.getElementById(guideId).classList.add('active');
            }
        });
    });

    // Initial calculation
    calculateDosage();
});
