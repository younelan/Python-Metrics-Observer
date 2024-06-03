<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{title}}</title>
    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <!-- Custom Styles -->
    {{pagestyle}} 
    <style>
        .article-img {

        height:130px;
        width:auto;
        margin:2px;
        float:right;
        }
        .left-article-img {
        margin:3px;
        float:left;
        height:130px;
        width:auto;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: {{pagebg}};
            color: {{pagefg}};
            margin: 0;
            padding: 0;
            height: 100%;
        }
        .navbar {
          background-color: {{menubg}};
          color: {{menufg}};
          padding: 15px 0;
        }
        .navbar-brand {
            font-weight: bold;
            font-size: 1.5rem;
        }
        .main-content {
            overflow: auto;
            background-color: #fff;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
            padding: 20px;
            margin-bottom: 30px;
            font-size: 1.1rem;
        }
        .footer {
            background-color: {{footerbg}};
            color: {{footerfg}};
            width: 100%;
            padding: 20px 0;
            text-align: center;
            position: fixed;
            bottom: 0;
        }
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-md navbar-dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="/{{sitepath}}">
                <img height=40 heigh=auto alt='{{title}}' src="{{sitepath}}/{{logoimg}}">
                
            </a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="true" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                {{navigationmenu}}
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <div class="container">
        <div class="main-content">
    {{pagebefore}}
    {{contentbefore}}
    {{content}}
    {{contentafter}}
    {{pageafter}}

        </div>
    </div>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            {{footer}}
        </div>
    </footer>

    <!-- Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
