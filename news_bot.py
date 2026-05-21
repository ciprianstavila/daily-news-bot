<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ziarul Meu Personal</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; color: #333; margin: 0; padding: 20px; display: none; }
        .container { max-width: 1100px; margin: 0 auto; }
        header { text-align: center; padding: 30px 0; border-bottom: 3px solid #3498db; margin-bottom: 30px; }
        h1 { margin: 0; color: #2c3e50; font-size: 2.5rem; }
        .date { color: #7f8c8d; margin-top: 5px; font-style: italic; }
        .category-section { margin-bottom: 40px; }
        h2 { color: #2c3e50; border-left: 5px solid #3498db; padding-left: 10px; margin-bottom: 20px; }
        .news-grid { display: block; }
        .news-card { background: white; padding: 20px; margin-bottom: 15px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
        .news-card h3 { margin-top: 0; color: #2980b9; font-size: 1.3rem; }
        .source { font-size: 0.85rem; color: #e67e22; font-weight: bold; }
        .news-card p { color: #555; line-height: 1.5; font-size: 0.95rem; }
        .read-btn { display: inline-block; background-color: #3498db; color: white; padding: 8px 15px; text-decoration: none; border-radius: 4px; font-size: 0.9rem; font-weight: bold; text-transform: uppercase; }
        .read-btn:hover { background-color: #2980b9; }
        .error { background-color: #fde8e8; color: #e74c3c; padding: 15px; border-radius: 5px; }
    </style>
    <script>
        function verificaParola() {
            var parolaCorecta = "[PAROLA]";
            var incercare = prompt("🔒 Acest site este privat. Introdu parola pentru a citi știrile:");
            
            if (incercare === parolaCorecta) {
                document.documentElement.style.display = "block";
                document.body.style.display = "block";
            } else {
                alert("❌ Parolă incorectă! Acces interzis.");
                window.location.href = "https://www.google.com";
            }
        }
        window.onload = verificaParola;
    </script>
</head>
<body>
    <div class='container'>
        <header>
            <h1>☕ Briefingul Tău Personal de Știri</h1>
            <div class='date'>Actualizat automat la data de: [DATA]</div>
        </header>
        
        [STIRI]
        
    </div>
</body>
</html>
