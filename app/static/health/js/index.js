function filterPlans() {
    var searchInput = document.getElementById('search-input').value.toLowerCase();
    var selectedGoal = document.getElementById('goal-filter').value.toLowerCase();
    var planWrappers = document.querySelectorAll('.plan-wrapper');

    planWrappers.forEach(function(plan) {
        var planName = plan.getAttribute('data-name').toLowerCase();
        var planGoal = plan.getAttribute('data-goal').toLowerCase();

        var nameMatch = planName.includes(searchInput);
        var goalMatch = selectedGoal === "" || planGoal === selectedGoal;

        if (nameMatch && goalMatch) {
            plan.style.display = 'block';
        } else {
            plan.style.display = 'none';
        }
    });
}
