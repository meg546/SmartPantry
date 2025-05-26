import 'package:flutter/material.dart';
import '../services/scanner.dart';

class AddItemScreen extends StatefulWidget {
  final String barcode;
  final String? suggestedName;
  final String? suggestedQuantityInfo;
  final String? productImageUrl;

  const AddItemScreen({
    Key? key,
    required this.barcode,
    this.suggestedName,
    this.suggestedQuantityInfo,
    this.productImageUrl,
  }) : super(key: key);

  @override
  State<AddItemScreen> createState() => _AddItemScreenState();
}

class _AddItemScreenState extends State<AddItemScreen> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  final _quantityController = TextEditingController();
  final _unitController = TextEditingController();
  
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    
    // Auto-populate from suggested data
    _nameController.text = widget.suggestedName ?? '';
    _quantityController.text = _extractQuantityFromInfo(widget.suggestedQuantityInfo) ?? '1';
    _unitController.text = _extractUnitFromInfo(widget.suggestedQuantityInfo) ?? 'units';
    
    print('Auto-populated name: ${_nameController.text}');
    print('Auto-populated quantity: ${_quantityController.text} ${_unitController.text}');
  }

  Future<void> _addItem() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() {
      _isLoading = true;
    });

    final success = await BarcodeService.addPantryItem(
      name: _nameController.text,
      quantity: int.parse(_quantityController.text),
      unit: _unitController.text,
      barcode: widget.barcode,
    );

    setState(() {
      _isLoading = false;
    });

    if (success) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Item added to pantry!')),
      );
      Navigator.of(context).pop();
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Failed to add item')),
      );
    }
  }

  // Helper method to extract quantity from string like "500g" or "12 oz"
  String? _extractQuantityFromInfo(String? quantityInfo) {
    if (quantityInfo == null || quantityInfo.isEmpty) return null;
    
    // Extract numbers from strings like "500g", "12 oz", "1.5L"
    final RegExp numberRegex = RegExp(r'(\d+\.?\d*)');
    final match = numberRegex.firstMatch(quantityInfo);
    return match?.group(1);
  }

  // Helper method to extract unit from string like "500g" or "12 oz"
  String? _extractUnitFromInfo(String? quantityInfo) {
    if (quantityInfo == null || quantityInfo.isEmpty) return null;
    
    // Extract unit from strings like "500g", "12 oz", "1.5L"
    final RegExp unitRegex = RegExp(r'(\d+\.?\d*)\s*([a-zA-Z]+)');
    final match = unitRegex.firstMatch(quantityInfo);
    return match?.group(2) ?? 'units';
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Add Pantry Item'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Product image if available
              if (widget.productImageUrl != null)
                Container(
                  height: 200,
                  margin: const EdgeInsets.only(bottom: 16),
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(color: Colors.grey[300]!),
                  ),
                  child: ClipRRect(
                    borderRadius: BorderRadius.circular(8),
                    child: Image.network(
                      widget.productImageUrl!,
                      fit: BoxFit.cover,
                      errorBuilder: (context, error, stackTrace) {
                        return const Icon(Icons.image_not_supported, size: 64);
                      },
                    ),
                  ),
                ),
              
              // Barcode display
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.grey[100],
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Row(
                  children: [
                    const Icon(Icons.qr_code),
                    const SizedBox(width: 8),
                    Text('Barcode: ${widget.barcode}'),
                  ],
                ),
              ),
              const SizedBox(height: 16),
              
              // Name field
              TextFormField(
                controller: _nameController,
                decoration: const InputDecoration(
                  labelText: 'Product Name',
                  border: OutlineInputBorder(),
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter a product name';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16),
              
              // Quantity field
              TextFormField(
                controller: _quantityController,
                decoration: const InputDecoration(
                  labelText: 'Quantity',
                  border: OutlineInputBorder(),
                ),
                keyboardType: TextInputType.number,
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter a quantity';
                  }
                  if (int.tryParse(value) == null || int.parse(value) <= 0) {
                    return 'Please enter a valid number';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16),
              
              // Unit field
              TextFormField(
                controller: _unitController,
                decoration: const InputDecoration(
                  labelText: 'Unit (e.g., pieces, lbs, bottles)',
                  border: OutlineInputBorder(),
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter a unit';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 24),
              
              // Add button
              ElevatedButton(
                onPressed: _isLoading ? null : _addItem,
                child: _isLoading
                    ? const CircularProgressIndicator()
                    : const Text('Add to Pantry'),
              ),
            ],
          ),
        ),
      ),
    );
  }

  @override
  void dispose() {
    _nameController.dispose();
    _quantityController.dispose();
    _unitController.dispose();
    super.dispose();
  }
}