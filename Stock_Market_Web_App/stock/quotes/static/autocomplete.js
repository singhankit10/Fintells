var $ = jQuery.noConflict();
$(document).ready(function() {
    // Listen for changes in the search input
    $('#ticker').on('input', function() {
        var input = $(this).val();
        if (input.length >= 2) { // allow search with 2 characters
            // Send a request to the Alpha Vantage API to retrieve matching symbols and company names
            $.get('https://www.alphavantage.co/query', {
                function: 'SYMBOL_SEARCH',
                keywords: input,
                datatype: 'json',
                apikey: 'B6NCGHAGK7NX1REI'
            }, function(response) {
                // Clear the previous autocomplete suggestions
                $('#autocomplete').empty();
                // Display the top 4 matching symbols and company names as autocomplete suggestions
                for (var i = 0; i < 4 && i < response.bestMatches.length; i++) {
                    var symbol = response.bestMatches[i]['1. symbol'];
                    var name = response.bestMatches[i]['2. name'];
                    $('#autocomplete').append('<div class="autocomplete-suggestion">' + symbol + ' - ' + name + '</div>');
                }
                // Listen for clicks on the autocomplete suggestions and fill the search input with the selected symbol
                $('.autocomplete-suggestion').on('click', function() {
                    var selected = $(this).text().split(' - ');
                    var symbol = selected[0];
                    var name = selected[1];
                    $('#ticker').val(symbol);
                    $('#autocomplete').empty();
                });
            });
        } else {
            $('#autocomplete').empty();
        }
    });
});
