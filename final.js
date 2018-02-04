// Check if the page is ready
$(document).ready( function() {
    // User searchs for a protein
    $('#submit').click( function() {

        runSearch();
        return false;  // prevents 'normal' form submission
    });
    // Calls to autocomplete the protein
    autocomplete();
});

// Dyanmical executes search using AJAX
function runSearch( term ) {
    // Hide and clear resutls for consecutive searches
    $('#results').hide();
    $('tbody').empty();
    $('#database').empty();

    // Pass user protein search to server
    var frmStr = $('#gene_search').serialize();
    
    $.ajax({
        url: './final.cgi',
        dataType: 'json',
        data: frmStr,
        success: function(data, textStatus, jqXHR) {
            processJSON(data);
        },
        error: function(jqXHR, textStatus, errorThrown){
            alert("Failed to perform gene search! textStatus: (" + textStatus +
              ") and errorThrown: (" + errorThrown + ")");
        }
    });
}

// Processes JSON opject from cgi file
function processJSON( data ) {
    // Calculates protein matches
    $('#match_count').text(data.match_count + ' Total Protein(s) Found' );
    // Adds information about genbank file to database table
    $('<tr><td id="db_element">Database:</td><td >' + data.match_name +'</td></tr>').appendTo('#database');
    $('<tr><td id="db_element">URL:</td><td>' + data.match_url +'</td></tr>').appendTo('#database');
    $('<tr><td id="db_element">Accession:</td><td>' + data.match_accession +'</td></tr>').appendTo('#database');
    $('<tr><td id="db_element">Version:</td><td>' + data.match_version +'</td></tr>').appendTo('#database');
    $('<tr><td id="db_element">Genus:</td><td>' + data.match_genus +'</td></tr>').appendTo('#database');
    $('<tr><td id="db_element">Species:</td><td>' + data.match_species +'</td></tr>').appendTo('#database');
    $('<tr><td id="db_element">Common Name:</td><td>' + data.match_common_name +'</td></tr>').appendTo('#database');
    
    // Tracks collapsible protein boxes
    var collapse_count = 1;

    // Clears the container for mutliple protein matches
    $("#container").empty();

    // Iterates through each protein match and creates a new collapsible box for it
    $.each(data.matches, function(key, val) {

        // Crates new container
        var accordion = '<div class="panel-group" id="accordion"><div class="panel panel-default"><div class="panel-heading"><h4 id="panel_title" class="panel-title"><a id="collapse_title" data-toggle="collapse" data-parent="#accordion" href="#collapse' + collapse_count + '">' + val.value + '</a></h4></div><div id="collapse' + collapse_count + '" class="panel-collapse collapse"><div id="panel_body' + collapse_count + '" class="panel-body"></div></div>';
        $(accordion).appendTo('#container')

        // Adds protein data to protein table
        var output = '<table id=output' + collapse_count + '>';

        output +='<tr><td>Uniquename:</td><td id="qualities">' + val.uniquename +'</td></tr>';
        output +='<tr><td>Residue:</td><td id="qualities">' + val.residues +'</td></tr>';
        output +='<tr><td>Residue Length:</td><td id="qualities">' + val.seqlen +'</td></tr>';
        output +='<tr><td>GC Content:</td><td id="qualities">' + val.gc +'</td></tr>';
        output +='<tr><td>Start:</td><td id="qualities">' + val.fmin +'</td></tr>';
        output +='<tr><td>End:</td><td id="qualities">' + val.fmax +'</td></tr>';
        output +='<tr><td>Strand:</td><td id="qualities">' + val.strand +'</td></tr>';
        output +='<tr><td>Protein Product:</td><td id="qualities">' + val.value +'</td></tr>';
        output +='<tr><td>Translation:</td><td id="qualities">' + val.translation +'</td></tr>';
        output +='<tr><td>Translation Length:</td><td id="qualities">' + val.translationlen +'</td></tr>';

        output += '</table>';
        $(output).appendTo('#panel_body' + collapse_count);

        collapse_count++;

    });

    // Moves search box from the center to the top of the screen above the search results
    $('#gene_search').css({"position": "absolute", "top": "1%", "left": "40%", "font-size": "18px"});
    
    // Shows hidden search results
    $('#results').show();

    // Shows hidden databases to search
    $('#databases').show();
}

// Suggests protein products that corresponds to the user input
function autocomplete() {
    $('#search_term').autocomplete({        
        source:function(request, response){ 
            $.ajax({
                url: './final.cgi',
                dataType: 'json', 
                data: {
                    search_term: request.term   
                },
                success: function(data, textStatus, jqXHR){
                    // Checks if no matches are found 
                    if(!data.matches.length){
                      var result = [
                      {
                       label: 'No proteins found', 
                       value: response.term
                   }
                   ];
                   response(result);
               }
                 // If matches are found the normal response is executed
                 else {
                            response( $.map(data.matches, function (results){  
                                return {
                                    label: results.value
                                }
                            }));
                        }
                    }
                });
        }
    });
}