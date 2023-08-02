const input = document.getElementById("input");
const alertContainer = document.getElementById("alert");
const messageTextArea = document.getElementById("message");

input.addEventListener("change", handleFiles);

function handleFiles() {
  const file = input.files[0];
  const reader = new FileReader();
  reader.readAsText(file);

  reader.onload = function () {
    const content = reader.result;
    Papa.parse(content, {
      header: true,
      complete: function (results) {
        const data = results.data;
        // Remove the call to validateCSV function for now
        // if (validateCSV(data)) {
        displayData(data);
        displaySuccess("Successfully loaded data from CSV file.");
        // } else {
        //   displayError("Invalid CSV format.");
        // }
      }
    });
  };
}

// Validate if the required fields (ContactNo, Boarder, Bed, and Leave) exist in the CSV data
function validateCSV(data) {
  const requiredFields = ["ContactNo", "Boarder", "Bed", "Leave"];
  const header = Object.keys(data[0]);

  // Check if all required fields exist in the header
  return requiredFields.every(field => header.includes(field));
}


function displayData(data) {
  // Clear the previous content of the message text area
  messageTextArea.value = '';

  for (const row of data) {
    // Iterate through each row and display all the properties in the message text area
    for (const property in row) {
      messageTextArea.value += `${property}: ${row[property]}\n`;
    }
    // Add a line break to separate each row
    messageTextArea.value += '\n';
  }
}

function displayError(message) {
  // Clear the content inside the alert container
  alertContainer.innerHTML = '';

  // Create a new success alert element
  const successAlert = document.createElement('div');
  successAlert.classList.add('bg-red-lighter', 'border', 'border-red-dark', 'text-red', 'px-4', 'py-3', 'rounded', 'relative', 'mt-2', 'mx-2', 'hover:bg-red-light', 'hover:text-white', 'hover:shadow-md');
  successAlert.setAttribute('role', 'alert');

  successAlert.innerHTML = `
    <strong class="font-bold">Error!</strong>
    <span class="block sm:inline">${message}</span>
  `;

  // Append the success alert element to the alert container
  alertContainer.appendChild(successAlert);
}

function displaySuccess(message) {
  // Clear the content inside the alert container
  alertContainer.innerHTML = '';

  // Create a new success alert element
  const successAlert = document.createElement('div');
  successAlert.classList.add('bg-green-lighter', 'border', 'border-green-dark', 'text-green', 'px-4', 'py-3', 'rounded', 'relative', 'mt-2', 'mx-2', 'hover:bg-green-light', 'hover:text-white', 'hover:shadow-md');
  successAlert.setAttribute('role', 'alert');

  successAlert.innerHTML = `
    <strong class="font-bold">Success!</strong>
    <span class="block sm:inline">${message}</span>
  `;

  // Append the success alert element to the alert container
  alertContainer.appendChild(successAlert);
}
