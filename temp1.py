import gmaps
 
gmaps.configure(api_key='AIzaSyBYkIz-pqehbEloeqad8C-JSvTgLruFdBg')
 
marker_locations = [
(-37.813323, 144.968645),
]
 
 
fig = gmaps.figure()
markers = gmaps.marker_layer(marker_locations)
fig.add_layer(markers)
fig