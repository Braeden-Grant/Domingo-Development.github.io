document.querySelector("form").addEventListener("submit", function(event) {
    let name = document.getElementById("name").value;
    let email = document.getElementById("email").value;
    let websiteType = document.querySelector('input[name="website-type"]:checked');
    let ecommerce = document.querySelector('input[name="ecommerce"]:checked');
    let physicalProducts = document.querySelector('input[name="physical-products"]:checked');
    let pagesNeeded = document.getElementById("pages-needed").value;
    let websiteNeeds = document.getElementById("website-needs").value;
    let newsSection = document.querySelector('input[name="news-section"]:checked');
    let contactOption = document.querySelector('input[name="contact-option"]:checked');
    let portfolio = document.querySelector('input[name="portfolio"]:checked');

    // Check if all required fields are filled
    if (!name || !email || !websiteType || !ecommerce || !physicalProducts || !pagesNeeded || !websiteNeeds || !newsSection || !contactOption || !portfolio) {
        alert("All fields are required!");
        event.preventDefault(); 
        return;
    }

    // Create a message summary for the submission
    let summaryMessage = `
        Name: ${name}\n
        Email: ${email}\n
        Questionnaire:\n
        1. Website Type: ${websiteType.value}\n
        2. E-commerce Solutions: ${ecommerce.value}\n
        3. Physical Products: ${physicalProducts.value}\n
        4. Pages Needed: ${pagesNeeded}\n
        5. Website Needs: ${websiteNeeds}\n
        6. News Section: ${newsSection.value}\n
        7. Contact Option: ${contactOption.value}\n
        8. Portfolio: ${portfolio.value}
    `;

    console.log(summaryMessage); // For debugging: View message in console
});
