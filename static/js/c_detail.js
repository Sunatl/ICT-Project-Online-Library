// Wait for the document to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Function to format numbers as currency
    function formatCurrency(amount) {
        return parseFloat(amount).toFixed(2) + ' сомонӣ';
    }

    // Add hover effect to purchase items
    const purchaseItems = document.querySelectorAll('li');
    purchaseItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.backgroundColor = '#f8f9fa';
            this.style.transition = 'background-color 0.3s';
        });

        item.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '';
        });
    });

    // Add animation to the total amount
    const totalUnpaid = document.querySelector('p strong');
    if (totalUnpaid) {
        totalUnpaid.style.transition = 'color 0.3s';
        totalUnpaid.addEventListener('mouseenter', function() {
            this.style.color = '#dc3545';
        });
        totalUnpaid.addEventListener('mouseleave', function() {
            this.style.color = '';
        });
    }

    // Add a search/filter functionality
    const searchBox = document.createElement('input');
    searchBox.type = 'text';
    searchBox.placeholder = 'Ҷустуҷӯи китоб...';
    searchBox.className = 'form-control mb-3';
    
    const purchaseList = document.querySelector('ul');
    if (purchaseList) {
        purchaseList.parentNode.insertBefore(searchBox, purchaseList);

        searchBox.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            const items = purchaseList.querySelectorAll('li');
            
            items.forEach(item => {
                const bookTitle = item.querySelector('strong').nextSibling.textContent.toLowerCase();
                if (bookTitle.includes(searchTerm)) {
                    item.style.display = '';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }

    // Add sort functionality
    const sortButton = document.createElement('button');
    sortButton.textContent = 'Мураттабсозӣ аз рӯи нарх';
    sortButton.className = 'btn btn-secondary mb-3 ms-2';
    
    if (purchaseList) {
        searchBox.parentNode.insertBefore(sortButton, purchaseList);
        
        let ascending = true;
        sortButton.addEventListener('click', function() {
            const items = Array.from(purchaseList.querySelectorAll('li'));
            
            items.sort((a, b) => {
                const priceA = parseFloat(a.textContent.match(/Нархи умумӣ: (\d+\.?\d*)/)[1]);
                const priceB = parseFloat(b.textContent.match(/Нархи умумӣ: (\d+\.?\d*)/)[1]);
                
                return ascending ? priceA - priceB : priceB - priceA;
            });
            
            ascending = !ascending;
            sortButton.textContent = ascending ? 
                'Мураттабсозӣ аз рӯи нарх ⬆️' : 
                'Мураттабсозӣ аз рӯи нарх ⬇️';
            
            items.forEach(item => purchaseList.appendChild(item));
        });
    }

    // Add print functionality
    const printButton = document.createElement('button');
    printButton.textContent = 'Чоп кардан';
    printButton.className = 'btn btn-primary mb-3 ms-2';
    
    if (purchaseList) {
        searchBox.parentNode.insertBefore(printButton, purchaseList);
        
        printButton.addEventListener('click', function() {
            window.print();
        });
    }

    // Add collapse/expand functionality for each purchase
    const purchaseDetails = document.querySelectorAll('li');
    purchaseDetails.forEach(detail => {
        detail.style.cursor = 'pointer';
        const content = detail.innerHTML;
        const summary = detail.querySelector('strong').textContent + 
                       detail.querySelector('strong').nextSibling.textContent;
        
        detail.innerHTML = `
            <div class="purchase-header">${summary}</div>
            <div class="purchase-content" style="display: none">${content}</div>
        `;

        detail.querySelector('.purchase-header').addEventListener('click', function() {
            const content = this.nextElementSibling;
            content.style.display = content.style.display === 'none' ? 'block' : 'none';
        });
    });
});
