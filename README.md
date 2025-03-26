Code for assigning passengers to drivers based on minimization of some cost function. Currently written for drivers and passengers living in the city of Cambridge, UK.

Can be paired with a Google Form which can be linked to a Google Sheet, then downloaded as a csv and interpreted in data_loader.py .

Plot below is generated from a simulated set of random names and postcodes, provided by ChatGPT queries. 

![alt text](https://github.com/kyleyhw/driver_assignment/blob/main/driver_assignment_plot.png?raw=true)

Planned updates:

1. Include pick up order within each car assignment by implementing travelling salesman brute force. This should still be polynomial runtime because cars are fixed in size; if the group is larger, the travelling salesman is simply run more times because cars do not get larger.

2. Quantify errors of this approximation, compared with full brute force travelling salesman solution.

3. Rewrite cost function to incorporate destination information.

4. Implement road distance instead of physical distance.

5. Different max car sizes for each car. Currently hardcoded at 3, assuming 4 seater including driver.
