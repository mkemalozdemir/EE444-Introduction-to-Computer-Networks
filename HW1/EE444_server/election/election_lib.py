import csv
           
#print(vote_data)            
def simulate_election(vote_data, parties, selected_region, party_percentages):
    # Get the number of seats in the selected region
    seats = vote_data[selected_region]['seats']
    
    # Initialize a dictionary to store the number of seats each party wins
    seat_counts = {party: 0 for party in parties}
    
    # Calculate the total number of votes cast in the selected region
    #total_votes = vote_data[selected_region]['votes']
    
    # Multiply each party's percentage of votes by the total number of votes to get the actual number of votes
    actual_votes = {party:  percentage for party, percentage in party_percentages.items()}
    
    # Perform the D'Hondt calculation to allocate seats to each party
    for i in range(seats):
        # Calculate the D'Hondt score for each party
        scores = {party: actual_votes[party] / (seat_counts[party] + 1) for party in parties}
        
        # Find the party with the highest D'Hondt score
        winning_party = max(scores, key=scores.get)
        
        # Allocate a seat to the winning party
        seat_counts[winning_party] += 1
    
    # Return the final seat counts for each party
    return seat_counts

# Example usage
#vote_data = {
#    'region1': {'seats': 5, 'votes': 10000},
#    'region2': {'seats': 3, 'votes': 5000}
#}
#
## Define the list of parties
#parties = ['party1', 'party2', 'party3']
#
## Select a region and specify the percentage of votes for each party
#selected_region = 'region1'
#party_percentages = {'party1': 40, 'party2': 30, 'party3': 30}
#
## Simulate the election and print the results
#seat_counts = simulate_election(vote_data, parties, selected_region, party_percentages)
#for party, seats in seat_counts.items():
#    print(f'{party}: {seats} seats')        