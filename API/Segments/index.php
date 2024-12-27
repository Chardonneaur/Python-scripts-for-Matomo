<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Select Segments</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
        th, td {
            border: 1px solid #ccc;
            padding: 10px;
            text-align: left;
        }
        th {
            background-color: #f4f4f4;
        }
        button {
            padding: 10px 15px;
            background-color: #007bff;
            color: #fff;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
        .button-group {
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <h1>Select Segments to Send to Matomo</h1>

    <div class="button-group">
        <button type="button" onclick="sendSegments()">Send Segments</button>
        <button type="button" onclick="deleteAllSegments()" style="background-color: red;">Delete All Segments</button>
    </div>

    <form id="segmentForm">
        <div class="form-group">
            <label for="matomoUrl">Matomo Instance URL:</label>
            <input type="text" id="matomoUrl" name="matomoUrl" required>
        </div>
        <div class="form-group">
            <label for="tokenAuth">Matomo Token:</label>
            <input type="text" id="tokenAuth" name="tokenAuth" required>
        </div>
        <div class="form-group">
            <label for="idSite">Site ID:</label>
            <input type="text" id="idSite" name="idSite" required>
        </div>

        <h3>Select Segments:</h3>
        <table>
            <thead>
                <tr>
                    <th><input type="checkbox" id="selectAll" onclick="toggleSelectAll()"> Select All</th>
                    <th>Segment Name</th>
                    <th>Definition</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><input type="checkbox" id="abandonedCart" name="segments" value="abandonedCart|visitEcommerceStatus==abandonedCart"></td>
                    <td>Abandoned Cart</td>
                    <td>visitEcommerceStatus==abandonedCart</td>
                </tr>
                <tr>
                    <td><input type="checkbox" id="ordered" name="segments" value="ordered|visitEcommerceStatus==ordered"></td>
                    <td>Ordered</td>
                    <td>visitEcommerceStatus==ordered</td>
                </tr>
                <tr>
                    <td><input type="checkbox" id="orderedThenAbandonedCart" name="segments" value="orderedThenAbandonedCart|visitEcommerceStatus==orderedThenAbandonedCart"></td>
                    <td>Ordered Then Abandoned Cart</td>
                    <td>visitEcommerceStatus==orderedThenAbandonedCart</td>
                </tr>
                <tr>
                    <td><input type="checkbox" id="returningCustomer" name="segments" value="returningCustomer|visitorType==returningCustomer"></td>
                    <td>Returning Customer</td>
                    <td>visitorType==returningCustomer</td>
                </tr>
                <tr>
                    <td><input type="checkbox" id="revenueLeftInCart" name="segments" value="Revenue Left In Cart|revenueAbandonedCart>0"></td>
                    <td>Revenue Left In Cart</td>
                    <td>revenueAbandonedCart>0</td>
                </tr>
                <tr>
                    <td><input type="checkbox" id="bounces" name="segments" value="bounces|actions<=1"></td>
                    <td>Bounces</td>
                    <td>actions<=1</td>
                </tr>
                <tr>
                    <td><input type="checkbox" id="desktop" name="segments" value="desktop|deviceType==desktop"></td>
                    <td>Desktop</td>
                    <td>deviceType==desktop</td>
                </tr>
                <tr>
                    <td><input type="checkbox" id="direct" name="segments" value="direct|referrerType==direct"></td>
                    <td>Direct</td>
                    <td>referrerType==direct</td>
                </tr>
                <tr>
                    <td><input type="checkbox" id="newVisitors" name="segments" value="new visitors|visitorType==new"></td>
                    <td>New Visitors</td>
                    <td>visitorType==new</td>
                </tr>
                <tr>
                    <td><input type="checkbox" id="returningVisitors" name="segments" value="returning visitors|visitorType==returning"></td>
                    <td>Returning Visitors</td>
                    <td>visitorType==returning</td>
                </tr>
                <tr>
                    <td><input type="checkbox" id="search" name="segments" value="search|referrerType==search"></td>
                    <td>Search</td>
                    <td>referrerType==search</td>
                </tr>
                <tr>
                    <td><input type="checkbox" id="smartphone" name="segments" value="smartphone|deviceType==smartphone"></td>
                    <td>Smartphone</td>
                    <td>deviceType==smartphone</td>
                </tr>
                <tr>
                    <td><input type="checkbox" id="social" name="segments" value="social|referrerType==social"></td>
                    <td>Social</td>
                    <td>referrerType==social</td>
                </tr>
                <tr>
                    <td><input type="checkbox" id="tablet" name="segments" value="tablet|deviceType==tablet"></td>
                    <td>Tablet</td>
                    <td>deviceType==tablet</td>
                </tr>
                <tr>
                    <td><input type="checkbox" id="unbounces" name="segments" value="unbounces|actions>=2"></td>
                    <td>Unbounces</td>
                    <td>actions>=2</td>
                </tr>
                <tr>
                    <td><input type="checkbox" id="website" name="segments" value="website|referrerType==website"></td>
                    <td>Website</td>
                    <td>referrerType==website</td>
                </tr>
            </tbody>
        </table>

        <div class="button-group">
            <button type="button" onclick="sendSegments()">Send Segments</button>
            <button type="button" onclick="deleteAllSegments()" style="background-color: red;">Delete All Segments</button>
        </div>
    </form>

    <script>
        function toggleSelectAll() {
            const selectAllCheckbox = document.getElementById('selectAll');
            const checkboxes = document.querySelectorAll('input[name="segments"]');
            checkboxes.forEach(checkbox => checkbox.checked = selectAllCheckbox.checked);
        }

        function sendSegments() {
            const matomoUrl = document.getElementById('matomoUrl').value;
            const tokenAuth = document.getElementById('tokenAuth').value;
            const idSite = document.getElementById('idSite').value;

            const selectedSegments = Array.from(document.querySelectorAll('input[name="segments"]:checked'))
                .map(input => input.value.split('|'));

            if (!matomoUrl || !tokenAuth || !idSite || selectedSegments.length === 0) {
                alert('Please fill all fields and select at least one segment.');
                return;
            }

            selectedSegments.forEach(([name, definition]) => {
                const url = `${matomoUrl}?module=API&method=SegmentEditor.add&name=${encodeURIComponent(name)}&definition=${encodeURIComponent(definition)}&idSite=${idSite}&autoArchive=1&enabledAllUsers=1&token_auth=${tokenAuth}`;
                fetch(url, { method: 'POST' })
                    .then(response => {
                        if (response.ok) {
                            console.log(`Segment '${name}' added successfully.`);
                        } else {
                            console.error(`Failed to add segment '${name}'.`);
                        }
                    })
                    .catch(error => console.error('Error:', error));
            });

            alert('Segments have been sent. Check the console for details.');
        }

        function deleteAllSegments() {
            const matomoUrl = document.getElementById('matomoUrl').value;
            const tokenAuth = document.getElementById('tokenAuth').value;

            if (!matomoUrl || !tokenAuth) {
                alert('Please fill in the Matomo URL and Token Auth fields.');
                return;
            }

            const urlGetAllSegments = `${matomoUrl}?module=API&method=SegmentEditor.getAll&idSite=&format=JSON&token_auth=${tokenAuth}`;

            fetch(urlGetAllSegments)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Failed to fetch segments. Please check the Matomo URL and token.');
                    }
                    return response.json();
                })
                .then(data => {
                    const segments = data || [];

                    if (segments.length === 0) {
                        alert('No segments found to delete.');
                        return;
                    }

                    let completed = 0;

                    segments.forEach(segment => {
                        const urlDeleteSegment = `${matomoUrl}?module=API&method=SegmentEditor.delete&idSegment=${segment.idsegment}&token_auth=${tokenAuth}`;
                        fetch(urlDeleteSegment, { method: 'POST' })
                            .then(response => {
                                if (response.ok) {
                                    console.log(`Segment '${segment.name}' deleted successfully.`);
                                } else {
                                    console.error(`Failed to delete segment '${segment.name}'.`);
                                }
                            })
                            .catch(error => console.error('Error:', error))
                            .finally(() => {
                                completed++;
                                if (completed === segments.length) {
                                    alert('All segments deletion process is complete. Check the console for details.');
                                }
                            });
                    });
                })
                .catch(error => {
                    console.error('Error fetching segments:', error);
                    alert('Failed to fetch or delete segments. Check the console for details.');
                });
        }
    </script>
</body>
</html>
