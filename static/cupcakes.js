const BASE_URL = 'http://localhost:5000/api'

function generateCupcakeHTMl(cupcake) {
  return `
    <li cupcake-id=${cupcake.id} id='cupcake${cupcake.id}'>
      <img class='cupcake-image' src='${cupcake.image}' alt='${cupcake.flavor} cupcake'>
      <p class='cupcake${cupcake.id}-text'>
        ${cupcake.flavor}<br>
        Size: ${cupcake.size}<br>
        Rating: ${cupcake.rating}<br>
      </p>
      <button class='delete-btn'>Delete Cupcake</button>
    </li>
  `
}

async function listingCupcakes() {
  const response = await axios.get(`${BASE_URL}/cupcakes`);
  console.log(response)
  for(let cupcakeData of response.data.cupcakes) {
    let cupcake = generateCupcakeHTMl(cupcakeData);
    $('.cupcakes-list').append(cupcake)
  }
}

$('.add-cupcake-form').on('submit', async function(event) {
  event.preventDefault();

  let flavor = $('#flavor').val();
  let size = $('#size').val();
  let rating = $('#rating').val();
  let image = $('#image').val();

  const response = await axios.post(`${BASE_URL}/cupcakes`, {flavor, size, rating, image});

  let newCupcake = generateCupcakeHTMl(response.data.cupcake);
  $('.cupcakes-list').append(newCupcake);
  $('.add-cupcake-form').trigger('reset')
})

$('.cupcakes-list').on('click', '.delete-btn', async function(event) {
  event.preventDefault();
  let $cupcake = $(event.target).closest('li');
  let cupcakeId = $cupcake.attr('cupcake-id');

  await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
  $cupcake.remove()

})

$(listingCupcakes)