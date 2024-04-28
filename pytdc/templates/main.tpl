<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Server Tower Periscope</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>
        /* Custom styles can be added here */
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f8f9fa;
            color: #343a40;
            padding-top: 56px;
        }

        .navbar {
            background-color: #007bff;
        }

        .navbar-brand {
            color: #ffffff;
        }

        .navbar-nav .nav-link {
            color: #ffffff;
        }

        .content {
            margin-top: 20px;
        }

        @media (max-width: 768px) {
            /* Custom styles for mobile devices can be added here */
            body {
                padding-top: 0;
            }
        }
    </style>
</head>

<body>
    <!-- Navigation Bar -->
    <nav class="navbar navbar-expand-lg navbar-dark fixed-top">
        <div class="container">
            <a class="navbar-brand" href="#">{{pagetitle}}</a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav"
                aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ml-auto">
                    <!-- Navigation menu items will be substituted here -->
                    {{ navigationmenu }}
                </ul>
            </div>
        </div>
    </nav>

    <!-- Content Section -->
    <div class="container content">
        <!-- Content will be substituted here -->
        {{ content }}
    </div>

    <!-- Bootstrap JS CDN -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.4/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>

</html>

