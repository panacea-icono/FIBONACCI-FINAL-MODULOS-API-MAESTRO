#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎨 MENÚ INTERACTIVO - PALETA DE OPCIONES
FIBONACCI MEDICAL API

Menú interactivo para seleccionar y configurar opciones de análisis
de superficie, mallas y mapeo de piel con IA.
"""

import json
from typing import Dict, Any
from surface_analysis_palette import SurfaceAnalysisPalette


class InteractivePaletteMenu:
    """Menú interactivo para la paleta de opciones"""

    def __init__(self):
        self.palette = SurfaceAnalysisPalette()
        self.selected_options = []
        self.user_requirements = {}

    def display_main_menu(self):
        """Muestra el menú principal"""
        print("\n" + "="*80)
        print("🎨 PALETA DE OPCIONES - ANÁLISIS DE SUPERFICIE Y MAPEO DE PIEL")
        print("="*80)
        print("1. 📋 Ver todas las categorías")
        print("2. 🔍 Explorar opciones por categoría")
        print("3. 💡 Obtener recomendaciones por caso de uso")
        print("4. 🎯 Crear plan personalizado")
        print("5. 📊 Comparar opciones")
        print("6. 💰 Ver opciones por precio")
        print("7. ⚡ Ver opciones por complejidad")
        print("8. 📝 Ver detalles de opción específica")
        print("9. 🛒 Agregar opción al carrito")
        print("10. 🛍️ Ver carrito de opciones")
        print("11. 📤 Exportar configuración")
        print("12. ❌ Salir")
        print("="*80)

    def display_categories(self):
        """Muestra todas las categorías disponibles"""
        print("\n📋 CATEGORÍAS DISPONIBLES:")
        print("-" * 50)

        for category_id, category_info in self.palette.categories.items():
            print(f"{category_info['icon']} {category_info['name']}")
            print(f"   {category_info['description']}")
            print()

    def explore_category(self):
        """Explora opciones por categoría"""
        print("\n🔍 EXPLORAR POR CATEGORÍA:")
        print("-" * 50)

        # Mostrar categorías disponibles
        categories = list(self.palette.categories.keys())
        for i, category_id in enumerate(categories, 1):
            category_info = self.palette.categories[category_id]
            print(f"{i}. {category_info['icon']} {category_info['name']}")

        try:
            choice = int(input("\nSelecciona una categoría (número): ")) - 1
            if 0 <= choice < len(categories):
                selected_category = categories[choice]
                self._display_category_options(selected_category)
            else:
                print("❌ Opción inválida")
        except ValueError:
            print("❌ Por favor ingresa un número válido")

    def _display_category_options(self, category_id: str):
        """Muestra las opciones de una categoría específica"""
        category_info = self.palette.categories[category_id]
        options = self.palette.get_options_by_category(category_id)

        print(f"\n{category_info['icon']} {category_info['name']}:")
        print("-" * 50)

        for option_id, option in options.items():
            print(f"• {option.name}")
            print(f"  Descripción: {option.description}")
            print(
                f"  Complejidad: {option.complexity} | "
                f"Tiempo: {option.processing_time} | "
                f"Precisión: {option.accuracy}"
            )
            print(f"  Precio: {option.price_tier}")
            print(f"  Casos de uso: {', '.join(option.use_cases)}")
            print()

    def get_recommendations(self):
        """Obtiene recomendaciones por caso de uso"""
        print("\n💡 RECOMENDACIONES POR CASO DE USO:")
        print("-" * 50)

        use_cases = list(self.palette.recommendations.keys())
        for i, use_case in enumerate(use_cases, 1):
            print(f"{i}. {use_case.upper()}")

        try:
            choice = int(input("\nSelecciona un caso de uso (número): ")) - 1
            if 0 <= choice < len(use_cases):
                selected_use_case = use_cases[choice]
                self._display_recommendations(selected_use_case)
            else:
                print("❌ Opción inválida")
        except ValueError:
            print("❌ Por favor ingresa un número válido")

    def _display_recommendations(self, use_case: str):
        """Muestra las recomendaciones para un caso de uso"""
        recommendations = self.palette.get_recommendations_for_use_case(use_case)

        print(f"\n💡 RECOMENDACIONES PARA {use_case.upper()}:")
        print("-" * 50)

        for rec_id in recommendations:
            option = self.palette.get_option_details(rec_id)
            if option:
                print(f"• {option.name}")
                print(f"  {option.description}")
                print(f"  Complejidad: {option.complexity} | Precio: {option.price_tier}")
                print()

    def create_custom_plan(self):
        """Crea un plan personalizado"""
        print("\n🎯 CREAR PLAN PERSONALIZADO:")
        print("-" * 50)

        # Recopilar requisitos del usuario
        requirements = {}

        print("Por favor responde las siguientes preguntas:")

        # Tipo de análisis
        print("\n1. ¿Qué tipo de análisis necesitas?")
        print("   a) Análisis de superficie")
        print("   b) Mapeo de piel")
        print("   c) Análisis de mallas 3D")
        print("   d) Detección de anomalías")
        print("   e) Múltiples tipos")

        analysis_type = input("Selecciona (a-e): ").lower()
        requirements["analysis_type"] = analysis_type

        # Complejidad
        print("\n2. ¿Qué nivel de complejidad prefieres?")
        print("   a) Básico (rápido, menos preciso)")
        print("   b) Medio (balanceado)")
        print("   c) Avanzado (lento, muy preciso)")

        complexity = input("Selecciona (a-c): ").lower()
        requirements["complexity"] = complexity

        # Presupuesto
        print("\n3. ¿Cuál es tu presupuesto?")
        print("   a) Gratuito")
        print("   b) Básico (hasta $100/mes)")
        print("   c) Premium (hasta $500/mes)")
        print("   d) Enterprise (sin límite)")

        budget = input("Selecciona (a-d): ").lower()
        requirements["budget"] = budget

        # Tiempo de procesamiento
        print("\n4. ¿Qué tan rápido necesitas los resultados?")
        print("   a) Muy rápido (segundos)")
        print("   b) Rápido (minutos)")
        print("   c) Medio (horas)")
        print("   d) No importa el tiempo")

        processing_time = input("Selecciona (a-d): ").lower()
        requirements["processing_time"] = processing_time

        # Crear plan personalizado
        plan = self._generate_custom_plan(requirements)
        self._display_custom_plan(plan)

    def _generate_custom_plan(self, requirements: Dict[str, str]) -> Dict[str, Any]:
        """Genera un plan personalizado basado en requisitos"""
        plan = {
            "recommended_options": [],
            "alternative_options": [],
            "estimated_cost": 0,
            "estimated_time": 0,
            "complexity": "low"
        }

        # Filtrar opciones basado en requisitos
        all_options = self.palette.get_all_options()

        for option_id, option in all_options.items():
            # Verificar complejidad
            if requirements["complexity"] == "a" and option.complexity != "low":
                continue
            elif requirements["complexity"] == "b" and option.complexity == "high":
                continue

            # Verificar presupuesto
            if requirements["budget"] == "a" and option.price_tier != "free":
                continue
            elif requirements["budget"] == "b" and option.price_tier in ["premium", "enterprise"]:
                continue
            elif requirements["budget"] == "c" and option.price_tier == "enterprise":
                continue

            # Verificar tiempo de procesamiento
            if requirements["processing_time"] == "a" and option.processing_time != "fast":
                continue
            elif requirements["processing_time"] == "b" and option.processing_time == "slow":
                continue

            # Agregar a recomendaciones
            if len(plan["recommended_options"]) < 3:
                plan["recommended_options"].append(option_id)
            else:
                plan["alternative_options"].append(option_id)

        return plan

    def _display_custom_plan(self, plan: Dict[str, Any]):
        """Muestra el plan personalizado"""
        print("\n🎯 TU PLAN PERSONALIZADO:")
        print("-" * 50)

        print("RECOMENDACIONES PRINCIPALES:")
        for option_id in plan["recommended_options"]:
            option = self.palette.get_option_details(option_id)
            if option:
                print(f"• {option.name}")
                print(f"  {option.description}")
                print(f"  Precio: {option.price_tier} | Complejidad: {option.complexity}")
                print()

        if plan["alternative_options"]:
            print("ALTERNATIVAS:")
            for option_id in plan["alternative_options"][:3]:  # Mostrar solo 3 alternativas
                option = self.palette.get_option_details(option_id)
                if option:
                    print(f"• {option.name}")
                    print(f"  Precio: {option.price_tier} | Complejidad: {option.complexity}")
                    print()

    def compare_options(self):
        """Compara opciones seleccionadas"""
        if len(self.selected_options) < 2:
            print("❌ Necesitas seleccionar al menos 2 opciones para comparar")
            return

        print("\n📊 COMPARACIÓN DE OPCIONES:")
        print("-" * 80)

        # Crear tabla de comparación
        print(f"{'Opción':<30} {'Complejidad':<12} {'Tiempo':<10} {'Precisión':<12} {'Precio':<10}")
        print("-" * 80)

        for option_id in self.selected_options:
            option = self.palette.get_option_details(option_id)
            if option:
                print(
                    f"{option.name[:29]:<30} {option.complexity:<12} {option.processing_time:<10} "
                    f"{option.accuracy:<12} {option.price_tier:<10}"
                )

    def filter_by_price(self):
        """Filtra opciones por precio"""
        print("\n💰 FILTRAR POR PRECIO:")
        print("-" * 50)
        print("1. Gratuito")
        print("2. Básico")
        print("3. Premium")
        print("4. Enterprise")

        try:
            choice = int(input("Selecciona un nivel de precio (1-4): "))
            price_tiers = ["free", "basic", "premium", "enterprise"]

            if 1 <= choice <= 4:
                selected_tier = price_tiers[choice - 1]
                options = self.palette.get_options_by_price_tier(selected_tier)

                print(f"\n💰 OPCIONES DE PRECIO {selected_tier.upper()}:")
                print("-" * 50)

                for option_id, option in options.items():
                    print(f"• {option.name}")
                    print(f"  {option.description}")
                    print(f"  Complejidad: {option.complexity} | Tiempo: {option.processing_time}")
                    print()
            else:
                print("❌ Opción inválida")
        except ValueError:
            print("❌ Por favor ingresa un número válido")

    def filter_by_complexity(self):
        """Filtra opciones por complejidad"""
        print("\n⚡ FILTRAR POR COMPLEJIDAD:")
        print("-" * 50)
        print("1. Baja (rápido, básico)")
        print("2. Media (balanceado)")
        print("3. Alta (lento, avanzado)")

        try:
            choice = int(input("Selecciona un nivel de complejidad (1-3): "))
            complexities = ["low", "medium", "high"]

            if 1 <= choice <= 3:
                selected_complexity = complexities[choice - 1]
                options = self.palette.get_options_by_complexity(selected_complexity)

                print(f"\n⚡ OPCIONES DE COMPLEJIDAD {selected_complexity.upper()}:")
                print("-" * 50)

                for option_id, option in options.items():
                    print(f"• {option.name}")
                    print(f"  {option.description}")
                    print(f"  Precio: {option.price_tier} | Tiempo: {option.processing_time}")
                    print()
            else:
                print("❌ Opción inválida")
        except ValueError:
            print("❌ Por favor ingresa un número válido")

    def show_option_details(self):
        """Muestra detalles de una opción específica"""
        print("\n📝 DETALLES DE OPCIÓN:")
        print("-" * 50)

        # Mostrar opciones disponibles
        all_options = self.palette.get_all_options()
        option_list = list(all_options.keys())

        for i, option_id in enumerate(option_list, 1):
            option = all_options[option_id]
            print(f"{i}. {option.name}")

        try:
            choice = int(input("\nSelecciona una opción (número): ")) - 1
            if 0 <= choice < len(option_list):
                selected_option_id = option_list[choice]
                option = all_options[selected_option_id]

                print(f"\n📝 DETALLES DE {option.name.upper()}:")
                print("-" * 50)
                print(f"ID: {option.id}")
                print(f"Descripción: {option.description}")
                print(f"Categoría: {option.category}")
                print(f"Complejidad: {option.complexity}")
                print(f"Tiempo de procesamiento: {option.processing_time}")
                print(f"Precisión: {option.accuracy}")
                print(f"Nivel de precio: {option.price_tier}")
                print(f"Requisitos: {', '.join(option.requirements)}")
                print(f"Salidas: {', '.join(option.outputs)}")
                print(f"Casos de uso: {', '.join(option.use_cases)}")
            else:
                print("❌ Opción inválida")
        except ValueError:
            print("❌ Por favor ingresa un número válido")

    def add_to_cart(self):
        """Agrega una opción al carrito"""
        print("\n🛒 AGREGAR AL CARRITO:")
        print("-" * 50)

        # Mostrar opciones disponibles
        all_options = self.palette.get_all_options()
        option_list = list(all_options.keys())

        for i, option_id in enumerate(option_list, 1):
            option = all_options[option_id]
            print(f"{i}. {option.name}")

        try:
            choice = int(input("\nSelecciona una opción para agregar (número): ")) - 1
            if 0 <= choice < len(option_list):
                selected_option_id = option_list[choice]
                if selected_option_id not in self.selected_options:
                    self.selected_options.append(selected_option_id)
                    option = all_options[selected_option_id]
                    print(f"✅ {option.name} agregado al carrito")
                else:
                    print("⚠️ Esta opción ya está en tu carrito")
            else:
                print("❌ Opción inválida")
        except ValueError:
            print("❌ Por favor ingresa un número válido")

    def view_cart(self):
        """Muestra el carrito de opciones"""
        print("\n🛍️ TU CARRITO DE OPCIONES:")
        print("-" * 50)

        if not self.selected_options:
            print("Tu carrito está vacío")
            return

        for i, option_id in enumerate(self.selected_options, 1):
            option = self.palette.get_option_details(option_id)
            if option:
                print(f"{i}. {option.name}")
                print(f"   Precio: {option.price_tier} | Complejidad: {option.complexity}")
                print()

        print(f"Total de opciones: {len(self.selected_options)}")

    def export_configuration(self):
        """Exporta la configuración actual"""
        if not self.selected_options:
            print("❌ No hay opciones seleccionadas para exportar")
            return

        config = {
            "selected_options": [],
            "configuration": {
                "timestamp": "2024-01-01T00:00:00Z",
                "version": "1.0.0",
                "description": "Configuración personalizada de análisis de superficie"
            }
        }

        for option_id in self.selected_options:
            option = self.palette.get_option_details(option_id)
            if option:
                config["selected_options"].append({
                    "id": option.id,
                    "name": option.name,
                    "description": option.description,
                    "category": option.category,
                    "complexity": option.complexity,
                    "processing_time": option.processing_time,
                    "accuracy": option.accuracy,
                    "price_tier": option.price_tier,
                    "requirements": option.requirements,
                    "outputs": option.outputs,
                    "use_cases": option.use_cases
                })

        filename = "surface_analysis_configuration.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        print(f"✅ Configuración exportada a {filename}")

    def run(self):
        """Ejecuta el menú interactivo"""
        while True:
            self.display_main_menu()

            try:
                choice = int(input("\nSelecciona una opción (1-12): "))

                if choice == 1:
                    self.display_categories()
                elif choice == 2:
                    self.explore_category()
                elif choice == 3:
                    self.get_recommendations()
                elif choice == 4:
                    self.create_custom_plan()
                elif choice == 5:
                    self.compare_options()
                elif choice == 6:
                    self.filter_by_price()
                elif choice == 7:
                    self.filter_by_complexity()
                elif choice == 8:
                    self.show_option_details()
                elif choice == 9:
                    self.add_to_cart()
                elif choice == 10:
                    self.view_cart()
                elif choice == 11:
                    self.export_configuration()
                elif choice == 12:
                    print("👋 ¡Hasta luego!")
                    break
                else:
                    print("❌ Opción inválida. Por favor selecciona 1-12.")

                input("\nPresiona Enter para continuar...")

            except ValueError:
                print("❌ Por favor ingresa un número válido")
            except KeyboardInterrupt:
                print("\n👋 ¡Hasta luego!")
                break


if __name__ == "__main__":
    menu = InteractivePaletteMenu()
    menu.run()
