function toggleDescription(id) {
    const shortDesc = document.getElementById(`description-${id}`);
    const fullDesc = document.getElementById(`full-description-${id}`);
    if (shortDesc.style.display === "none") {
        shortDesc.style.display = "inline";
        fullDesc.style.display = "none";
    } else {
        shortDesc.style.display = "none";
        fullDesc.style.display = "inline";
    }
}

function filterTable() {
    const input = document.getElementById('search-input');
    const filter = input.value.toLowerCase().trim();
    const statusFilter = document.getElementById('status-filter').value.toLowerCase().trim();
    const table = document.querySelector('.table');
    const rows = table.getElementsByTagName('tr');

    console.log('Search Filter:', filter);
    console.log('Status Filter:', statusFilter);

    for (let i = 1; i < rows.length; i++) { // Start from 1 to skip the header row
        const cells = rows[i].getElementsByTagName('td');
        let shouldShow = true;

        // Filter by event name
        let nameMatches = false;
        for (let j = 0; j < cells.length; j++) {
            if (cells[j]) {
                const textValue = cells[j].textContent || cells[j].innerText;
                if (textValue.toLowerCase().indexOf(filter) > -1) {
                    nameMatches = true;
                    break;
                }
            }
        }

        // Filter by status
        const statusCell = cells[6]; // Assuming status is in the 7th column (index 6)
        let statusMatches = true;
        if (statusFilter) {
            // Get the selected option's value from the <select> element
            const selectElement = statusCell.querySelector('select');
            const selectedStatus = selectElement ? selectElement.value.toLowerCase() : '';
            console.log('Row', i, 'Selected Status:', selectedStatus, 'Matches:', selectedStatus === statusFilter);
            statusMatches = selectedStatus === statusFilter;
        }

        // Determine if the row should be displayed
        shouldShow = nameMatches && statusMatches;

        console.log('Row', i, 'Name Matches:', nameMatches, 'Should Show:', shouldShow);
        rows[i].style.display = shouldShow ? '' : 'none';
    }
}
