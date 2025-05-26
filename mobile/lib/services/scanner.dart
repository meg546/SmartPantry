import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter_dotenv/flutter_dotenv.dart';

class BarcodeService {
  // Use environment variables
  static String get baseUrl => dotenv.env['API_BASE_URL'] ?? 'http://localhost:8000';
  static String get openFoodFactsUrl => dotenv.env['OPENFOODFACTS_URL'] ?? 'https://world.openfoodfacts.org/api/v0/product';
  
  static Future<Map<String, dynamic>?> getProductInfo(String barcode) async {
    try {
      print('Fetching product info for barcode: $barcode');
      print('Using OpenFoodFacts URL: $openFoodFactsUrl');
      
      final response = await http.get(
        Uri.parse('$openFoodFactsUrl/$barcode.json'),
        headers: {'Content-Type': 'application/json'},
      ).timeout(Duration(seconds: 10));
      
      print('API Response status: ${response.statusCode}');
      
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        
        if (data['status'] == 1) {
          final product = data['product'];
          print('Product found: ${product['product_name']}');
          
          return {
            'name': product['product_name'] ?? 'Unknown Product',
            'brand': product['brands'] ?? '',
            'quantity_info': product['quantity'] ?? '',
            'image_url': product['image_url'] ?? '',
          };
        } else {
          print('Product not found in OpenFoodFacts database');
        }
      }
      return null;
    } catch (e) {
      print('Error fetching product info: $e');
      return null;
    }
  }
  
  static Future<bool> addPantryItem({
    required String name,
    required int quantity,
    required String unit,
    required String barcode,
  }) async {
    try {
      print('Adding item to backend: $baseUrl/pantry-items/');
      
      final response = await http.post(
        Uri.parse('$baseUrl/pantry-items/'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'name': name,
          'quantity': quantity,
          'unit': unit,
          'added_date': DateTime.now().toIso8601String(),
          'barcode': barcode,
        }),
      );
      
      print('📡 Backend response: ${response.statusCode}');
      
      if (response.statusCode == 200) {
        print('Successfully added to pantry');
        return true;
      } else {
        print('Failed to add to pantry: ${response.body}');
        return false;
      }
    } catch (e) {
      print('Error adding pantry item: $e');
      return false;
    }
  }

  static Future<List<Map<String, dynamic>>> getPantryItems() async {
    try {
      print('Fetching pantry items from: $baseUrl/pantry-items/');
      
      final response = await http.get(
        Uri.parse('$baseUrl/pantry-items/'),
        headers: {'Content-Type': 'application/json'},
      );
      
      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        print('Retrieved ${data.length} pantry items');
        return data.cast<Map<String, dynamic>>();
      }
      return [];
    } catch (e) {
      print('Error fetching pantry items: $e');
      return [];
    }
  }
}
