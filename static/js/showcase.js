document.addEventListener('DOMContentLoaded', function() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const heritageDetail = document.getElementById('heritageDetail');
    let currentCategory = '剪纸';

    async function loadHeritageData(category) {
        try {
            heritageDetail.innerHTML = '<div class="detail-loading">加载中...</div>';
            
            const response = await fetch('/api/heritage-data');
            const data = await response.json();
            
            const heritage = data[category];
            
            if (heritage) {
                displayHeritageDetail(heritage);
            } else {
                heritageDetail.innerHTML = '<div class="detail-loading">暂无数据</div>';
            }
        } catch (error) {
            console.error('加载非遗数据失败:', error);
            heritageDetail.innerHTML = '<div class="detail-loading">加载失败，请稍后重试</div>';
        }
    }

    function displayHeritageDetail(heritage) {
        const techniquesHtml = heritage.techniques.map(t => `<span class="tag">${t}</span>`).join('');
        const regionsHtml = heritage.regions.map(r => `<span class="tag">${r}</span>`).join('');
        const imagesHtml = heritage.images.map(img => `
            <div class="image-item">
                ${img.image_url ? `<img src="${img.image_url}" alt="${img.title}" class="heritage-image">` : ''}
                <h4>${img.title}</h4>
                <p>${img.description}</p>
            </div>
        `).join('');

        heritageDetail.innerHTML = `
            <h2>${heritage.name}</h2>
            <p class="description">${heritage.description}</p>
            
            <div class="section">
                <h3>历史渊源</h3>
                <p>${heritage.history}</p>
            </div>
            
            <div class="section">
                <h3>技艺特点</h3>
                <div class="techniques">${techniquesHtml}</div>
            </div>
            
            <div class="section">
                <h3>主要流派/地区</h3>
                <div class="regions">${regionsHtml}</div>
            </div>
            
            <div class="section">
                <h3>代表作品</h3>
                <div class="images">${imagesHtml}</div>
            </div>
        `;
    }

    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            tabBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            currentCategory = this.dataset.category;
            loadHeritageData(currentCategory);
        });
    });

    loadHeritageData(currentCategory);
});
