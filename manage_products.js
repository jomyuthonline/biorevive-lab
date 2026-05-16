const API_BASE = 'http://localhost:17456/api/biorevive';

document.addEventListener('DOMContentLoaded', () => {
    const productForm = document.getElementById('product-form');
    const productList = document.getElementById('product-list');
    const formMsg = document.getElementById('form-msg');
    const btnRefresh = document.getElementById('btn-refresh');

    // Fetch and display products
    async function loadProducts() {
        try {
            productList.innerHTML = '<p style="color: #666;">กำลังโหลด...</p>';
            const res = await fetch(`${API_BASE}/products`);
            const data = await res.json();
            
            if (data.products && data.products.length > 0) {
                productList.innerHTML = data.products.map(p => `
                    <div class="product-card">
                        <div class="product-info">
                            <h4>${p.name}</h4>
                            <p>หมวดหมู่: ${p.category === 'liquid' ? 'สูตรน้ำ' : 'สูตรพรีเมียม'}</p>
                            <p>อัตราส่วน: ${p.dosageRate} ${p.dosageUnit}</p>
                        </div>
                        <button class="btn-delete" onclick="deleteProduct('${p.id}')">
                            <i class="fa-solid fa-trash"></i> ลบ
                        </button>
                    </div>
                `).join('');
            } else {
                productList.innerHTML = '<p style="color: #aaa;">ยังไม่มีสินค้าในระบบ</p>';
            }
        } catch (err) {
            console.error(err);
            productList.innerHTML = '<p style="color: #e74c3c;">เกิดข้อผิดพลาดในการเชื่อมต่อ API. ตรวจสอบว่ารันเซิร์ฟเวอร์อยู่หรือไม่ (port 17456)</p>';
        }
    }

    // Add new product
    productForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const payload = {
            name: document.getElementById('p-name').value,
            category: document.getElementById('p-category').value,
            dosageRate: parseFloat(document.getElementById('p-rate').value),
            dosageUnit: document.getElementById('p-unit').value,
        };

        try {
            const res = await fetch(`${API_BASE}/products`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (res.ok) {
                formMsg.style.display = 'block';
                productForm.reset();
                setTimeout(() => formMsg.style.display = 'none', 3000);
                loadProducts();
            } else {
                alert('เกิดข้อผิดพลาดในการบันทึกข้อมูล');
            }
        } catch (err) {
            console.error(err);
            alert('ไม่สามารถเชื่อมต่อ API ได้');
        }
    });

    // Delete product globally attached so onclick works
    window.deleteProduct = async (id) => {
        if (!confirm('ยืนยันการลบสินค้านี้?')) return;
        
        try {
            const res = await fetch(`${API_BASE}/products/${id}`, {
                method: 'DELETE'
            });
            if (res.ok) {
                loadProducts();
            }
        } catch (err) {
            console.error(err);
            alert('ไม่สามารถลบข้อมูลได้');
        }
    };

    btnRefresh.addEventListener('click', loadProducts);

    // Initial load
    loadProducts();
});
