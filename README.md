# 🧪 Автотест калькулятора с Allure и Автотест интернет-магазина с Allure

▶️ Запуск тестов
pytest test_calc_allure.py --alluredir=reports/allure_results -v
pytest test_purchase_allure.py --alluredir=reports/allure_results -v

📊 Генерация отчёта
allure generate reports/allure_results -o reports/allure_report --clean
allure open reports/allure_report

или одной строкой:
allure serve reports/allure_results

✅ Просмотр отчётов:
\reports\allure_report\index.html