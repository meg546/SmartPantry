import 'package:flutter/material.dart';
import '../services/scanner.dart';
import '../models/pantry_item.dart';

class PantryListScreen extends StatefulWidget {
  const PantryListScreen({Key? key}) : super(key: key);

  @override
  State<PantryListScreen> createState() => _PantryListScreenState();
}

class _PantryListScreenState extends State<PantryListScreen> {
  List<Map<String, dynamic>> _items = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadItems();
  }

  Future<void> _loadItems() async {
    try {
      final items = await BarcodeService.getPantryItems();
      
      // Check if widget is still mounted before calling setState
      if (mounted) {
        setState(() {
          _items = items;
          _isLoading = false;
        });
      }
    } catch (e) {
      print('Error loading pantry items: $e');
      
      // Check if widget is still mounted before calling setState
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return const Scaffold(
        body: Center(
          child: CircularProgressIndicator(),
        ),
      );
    }

    return Scaffold(
      appBar: AppBar(
        title: const Text('My Pantry'),
      ),
      body: _items.isEmpty
          ? const Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.inventory_2, size: 64, color: Colors.grey),
                  SizedBox(height: 16),
                  Text('Your pantry is empty'),
                  Text('Scan some items to get started!'),
                ],
              ),
            )
          : ListView.builder(
              itemCount: _items.length,
              itemBuilder: (context, index) {
                final item = _items[index];
                return ListTile(
                  leading: const Icon(Icons.inventory),
                  title: Text(item['name'] ?? 'Unknown Item'),
                  subtitle: Text('${item['quantity']} ${item['unit']}'),
                  trailing: Text(item['added_date'] ?? ''),
                );
              },
            ),
    );
  }
}