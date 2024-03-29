document.addEventListener("DOMContentLoaded", function() {
    const poolTable = document.getElementById('poolTable');
    const cueBall = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    cueBall.setAttribute('id', 'cueBall');
    cueBall.setAttribute('r', '10');
    cueBall.setAttribute('fill', 'white');
    poolTable.appendChild(cueBall);

    let isDragging = false;
    let startX, startY;
    let line;

    function calculateInitialVelocity(endX, endY) {
        // Calculate the difference between end position and cue ball position
        const diffX = endX - startX;
        const diffY = endY - startY;

        // Use the difference to compute initial velocity (example)
        const initialVelocityX = diffX * 10; // Multiply by appropriate constant
        const initialVelocityY = diffY * 10; // Multiply by appropriate constant

        // Call a function to send the initial velocity for further processing
        sendInitialVelocityToServer(initialVelocityX, initialVelocityY);
    }

    function sendInitialVelocityToServer(velocityX, velocityY) {
        const formData = new FormData();
        formData.append('initial_velocity_x', velocityX);
        formData.append('initial_velocity_y', velocityY);
    
        fetch('/handle_shot', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                return response.text();
            } else {
                throw new Error('Network response was not ok.');
            }
        })
        .then(data => {
            console.log('Server response:', data);
            // You can handle the server response here if needed
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    poolTable.addEventListener('mousedown', function(event) {
        isDragging = true;
        startX = event.clientX;
        startY = event.clientY;
        line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        line.setAttribute('stroke', 'black');
        line.setAttribute('stroke-width', '3');
        line.setAttribute('x1', cueBall.getAttribute('cx'));
        line.setAttribute('y1', cueBall.getAttribute('cy'));
        line.setAttribute('x2', startX);
        line.setAttribute('y2', startY);
        poolTable.appendChild(line);
    });

    poolTable.addEventListener('mousemove', function(event) {
        if (isDragging) {
            line.setAttribute('x2', event.clientX);
            line.setAttribute('y2', event.clientY);
        }
    });

    poolTable.addEventListener('mouseup', function(event) {
        if (isDragging) {
            isDragging = false;
            const endX = event.clientX;
            const endY = event.clientY;
            calculateInitialVelocity(endX, endY);
            poolTable.removeChild(line);
        }
    });
});
